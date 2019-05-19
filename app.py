import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["DBS_NAME"] = os.getenv("DBS_NAME")

mongo = PyMongo(app)
recipes=mongo.db.recipes

@app.route('/')
def home():
    return render_template("index.html")
    
@app.route('/find_recipes', methods=['GET', 'POST'])
def find_recipes(): 
    if request.method == 'POST':
        search_text = request.form.get("search_text")
        mongo.db.recipes.create_index([("$**", 'text')])
        cursor = mongo.db.recipes.find({ "$text": { "$search": search_text }})
        recipes = [recipe for recipe in cursor]
        return render_template("search_results.html", recipes=recipes)

    return render_template("search_results.html", recipes=mongo.db.recipes.find())
    
    
@app.route('/search_results')
def search_results():
    return render_template("search_results.html", recipes=mongo.db.recipes.find())
    
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view_recipe.html", recipe=the_recipe)
    
@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)