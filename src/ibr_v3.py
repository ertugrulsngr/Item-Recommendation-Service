import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import os

warnings.filterwarnings("ignore")

class Item_Based_Recommender():
    def __init__(self):
        self.read_data_files()
        self.create_index_for_books()
        self.create_ratings_matrix()
    
    def read_data_files(self):
        #read provided datas
        product_data_file = "ky_products.csv"
        ratings_data_file = "ky_ratings.csv"
        
        path = os.path.realpath(__file__)
        src_dir = os.path.dirname(path)
        data_dir = src_dir.replace("src", "data")

        products_data_path = os.path.join(data_dir, product_data_file)
        ratings_data_path = os.path.join(data_dir, ratings_data_file)

        self.books = pd.read_csv(products_data_path, sep=";", encoding="utf-8")
        self.ratings = pd.read_csv(ratings_data_path, encoding="utf-8")

    def create_index_for_books(self):
        self.ratings["user_index"] = self.ratings["customer_id"].astype("category").cat.codes
        self.ratings["product_index"] = self.ratings["product_id"].astype("category").cat.codes
    
    def create_ratings_matrix(self):
        #create index to access similart items while proccess
        self.ratings['rating'] = self.ratings['rating'].astype(float)
        ratings_mat_coo = coo_matrix((self.ratings["rating"], (self.ratings["product_index"], self.ratings["user_index"])))
        self.ratings_matrix = ratings_mat_coo.tocsr()
        self.weighted_scores()
    
        
    def weighted_scores(self):
        sums = self.ratings_matrix.sum(1).A # Find sum of each row. 
        sums=np.squeeze(sums) # convert Nx1 matrix to 1xN matrix. 
        counts=np.diff(self.ratings_matrix.indptr) # Find counts of ratings for each item.
        means=(sums/counts)-np.finfo(np.float32).eps # Find mean ratings for each item. Subtract epsilon to avoid zero vectors.
        mc = np.repeat(means, counts) # Create matrix that represent mean for each rating. ??
        
        self.ratings_matrix.data -= mc

    def find_similar_books(self, product_index, number_of_books=21):
        
        similarity = cosine_similarity(self.ratings_matrix[product_index, :], self.ratings_matrix).flatten()

        # n largest values but not sorted
        indicies = np.argpartition(similarity, -number_of_books)[-number_of_books:]

        # sort indicies according to similarity scores
        indicies = indicies[np.argsort(-similarity[indicies])]

        similar_items = self.ratings[self.ratings["product_index"].isin(indicies)].copy()
        similar_items.drop(["customer_id", "rating", "user_index"], axis=1, inplace=True)
        similar_items["score"] = similarity[similar_items["product_index"]]
        similar_items.drop_duplicates(subset=['product_index'], inplace=True)
        similar_items.sort_values(by="score", ascending=False, inplace=True)

        result =  {
            "success" : True,
            "data" : []
        }

        for product_id, score in zip(similar_items["product_id"], similar_items["score"]):
            result["data"].append(
                {"productId" : product_id, 
                "productName" : self.books[self.books["product_id"] == product_id]["name"].values[0], 
                "score": score
                }
            )
        
        return result
    
    def find_book_index_using_book_name(self, book_name):
        book_index = self.books.index[self.books["name"] == book_name]
        if (book_index.size<0):
            raise Exception("Product is not found !")
        elif (book_index.size > 1 ):
            print("Warning ! There are multiple books with this book_name")
        else:
            return book_index[0]

    def find_book_product_index(self, product_id):
        product_index = self.ratings[self.ratings["product_id"] == product_id]["product_index"]
        return product_index.values[0]

    def recommend_using_book_name(self, product_name, limit=21):
        try:
            book_index = self.find_book_index_using_book_name(product_name)
        except:
            return {"success" : False, "message" : "Book not found"}

        product_id = self.books.loc[book_index]["product_id"]
        return self.recommend_using_product_id(product_id, limit)

    def recommend_using_product_id(self, product_id, limit=21):
        try:
            product_id = int(product_id)
        except:
            return {"success" : False, "message" : "Can not convert product id to int !"}
        try:
            product_index = self.find_book_product_index(product_id)
        except:
            return {"success" : False, "message" : "Product is not in ratings data"}
 
        return self.find_similar_books(product_index, limit)

if __name__ == "__main__":
    recommmender = Item_Based_Recommender()
    while True:
        product_id = input("Product ID (q => quit):")
        if (product_id == "q"):
            break
        else:
            print(recommmender.recommend_using_product_id(int(product_id)))