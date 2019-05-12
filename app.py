import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)


MONGO_URI = os.getenv("MONGO_URI")
DBS_NAME = os.getenv("DBS_NAME")


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)