import pymongo
import os

MONGO_URI = os.getenv("MONGO_URI")
DBS_NAME = os.getenv("DBS_NAME")
COLLECTION_NAME = 'recipes'

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e
        
conn = mongo_connect(MONGO_URI)

coll = conn[DBS_NAME][COLLECTION_NAME]


# Insert one entry

new_doc = {'title': 'test apple pie', 'author': 'alexa', 'recipe_description': "This is a tasty apple filled treat, and it's so easy to make", 'main_ingredient': 'apple', 'ingredients': [{'ingredient':'apples', 'amount':'300g'}, {'ingredient':'sugar', 'amount': '100g'}], 'method': 'boil the apples and add the sugar, mix the two together...', 'vegan':True, 'dairy_free':False, 'gluten_free':False }

coll.insert(new_doc)


documents = coll.find()

for doc in documents:
    print(doc)



