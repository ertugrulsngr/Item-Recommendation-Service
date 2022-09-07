
# Item Recommendation Service

## Overview
It's a recommender service that written in Python. It Makes recommendations using user-product ratings and product details data. In this project, Collaborative Filtering (Item-Item) technique and Cosine Similarity algorithm is used to find similarities among products.


## Data Model
If you want to run project without editing source code, your data model should be like below. 

Product data separator = ';'
Ratings data separator = ',' 

Edit **ibr_v3.py**  if your data files separators different ( in function =>```Item_Based_Recommender.read_data_files ```).

### Product Data
This data **can change** due to what you want display about products details after recommender give you product ids.
|product_id (int)|name (string)
|--|-----
|1|exampleProductName

### Ratings Data
|customer_id (int)|product_id (int)|rating (int)
|--|-----|-
|1|exampleProductName|5



## Usage

Run "**recommender_service.py**" .
Now recommender run as service with default **port:8080**. You can send requests using browsers, postman or whatever you want.


### Methods
You can get recommendations sending product_id or product_name.

    localhost:8080/recommend?productId=PRODUCT_ID_HERE&limit=LIMIT_HERE

- **productId :** ID of the product that you want to find similar items.
- **limit:** Number of the recommends you want to get. (Optional. Default is 21) 

or 

	localhost:8080/recommend?productName=1984&limit=LIMIT_HERE
- **productName :** Name of the product that you want to find similar items.
- **limit:** Number of the recommends you want to get. (Optional. Default is 21) 

If there are products with the same product name in your data then recommender take the first matching product to make recommendations.

You can also recreate recommender model via sending request. With this request, new recommender object will be created. Recommender object will read data files and preparation process will be executed. It's useful if your data files has changed and if you want changes to be considered.

    localhost:8080/reinit_recommender

## Response Data
When you send a request to recommender service, than it will send you a response data. The response data is in JSON format.
- **`succcess: boolean`**
	Is process handled successfully or not.
	
- **`message : string`**
	Description about process.
	
If you send `recommend` request, also `data` key added to response data. It is an array of  recommended items sorted by similarity score.

- **`data: array[{productId : int, productName:string, score:int}, ...]`**
Score is the similarity score of the item.

## Dependencies
This project created with dependencies below. Any other versions of dependencies was not tested.

- Python 3.10.5
- pandas : 1.4.3
- numpy : 1.23.1
- sklearn : 1.1.1
- scipy : 1.8.1
- flask : 2.2.2
