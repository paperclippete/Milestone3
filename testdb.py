import pymongo
import os

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "myTestDB"
COLLECTION_NAME = 'Recipes'

MONGO_URI = os.getenv("MONGO_URI")
DBS_NAME = os.getenv("DBS_NAME")


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
"""
new_doc = {'first': 'douglas', 'last': 'adams', 'dob': '11/03/1952', 'hair_colour': 'grey', 'occupation': 'writer', 'nationality': 'english'}

coll.insert(new_doc)
"""

# Insert many entries
"""
new_docs = [{'first': 'terry', 'last': 'pratchett', 'gender': 'm', 'dob': '28/04/1948', 'hair_colour': 'not much', 'occupation': 'writer', 'nationality': 'english'},
{'first': 'george', 'last': 'rr martin', 'gender': 'm', 'dob': '20/09/1948', 'hair_colour': 'white', 'occupation': 'writer', 'nationality': 'american'}]

coll.insert_many(new_docs)
"""

documents = coll.find()

for doc in documents:
    print(doc)



