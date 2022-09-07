from ibr_v3 import Item_Based_Recommender
from flask import Flask, request

app = Flask(__name__)

recommender = Item_Based_Recommender()

@app.route('/')
@app.route('/recommend', methods=['GET'])
def recommend():
    productId = request.args.get("productId")
    productName = request.args.get("productName")
    limit = request.args.get("limit")
    if (limit == None):
        limit = 21
    else:
        try:
            limit = int(limit)
            if (limit == 0):
                limit = 21
        except:
            return {
            "success" : False,
            "message" : "Limit parameter must be an integer"
        }
    if  (productId != None):
        return recommender.recommend_using_product_id(productId, limit)
    elif (productName != None):
        return recommender.recommend_using_book_name(productName, limit)
    else:
        return {
            "success" : False,
            "message" : "Neither productId nor productName is provided"
        }

@app.route('/reinit_recommender', methods=['GET'])
def reinit_recommender():
    global recommender
    try:
        recommender = Item_Based_Recommender()
        return {"success" : True, "message" : "Recommender reinitialized"}
    except:
        return {"success" : False, "message" : "Error while reinitializing recommender"}

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)