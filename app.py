import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
"""from forms import recipe_search"""

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["DBS_NAME"] = os.getenv("DBS_NAME")

mongo = PyMongo(app)
recipes = mongo.db.recipes

@app.route('/')
def home():
    return render_template("index.html", recipes=recipes)
    
@app.route('/user_login')
def user_login():
    if request.method == 'POST':
        users =mongo.db.users
        login_user = users.find_one({'name' : request.form.get('username')})
    return render_template("user_home.html")
    
@app.route('/find_recipes', methods=['POST'])
def find_recipes():
    if request.method == 'POST':
        search_text = request.form.get("search_text")
        checkboxes = request.form.getlist("check")
        print(checkboxes)
        if len(checkboxes) == 0:
            cursor = mongo.db.recipes.find({ "$text": { "$search": search_text }})
            matching_recipes = [matching_recipe for matching_recipe in cursor]
            print("Hello 0")
        elif len(checkboxes) == 1:
            cursor = mongo.db.recipes.find({ "$and": [{ "$text": { "$search": search_text }}, { checkboxes[0]: True}, ] }) 
            matching_recipes = [matching_recipe for matching_recipe in cursor]
            print("Hello 1")
            
        elif len(checkboxes) == 2:
            cursor = mongo.db.recipes.find({ "$and": [{ "$text": { "$search": search_text }}, { checkboxes[0]: True}, { checkboxes[1]: True} ] }) 
            matching_recipes = [matching_recipe for matching_recipe in cursor]
            print("Hello 2")
            
        elif len(checkboxes) == 3:
            cursor = mongo.db.recipes.find({ "$and": [{ "$text": { "$search": search_text }}, { checkboxes[0]: True}, { checkboxes[1]: True}, { checkboxes[2]: True} ] }) 
            matching_recipes = [matching_recipe for matching_recipe in cursor]
            print("Hello 3")
              
        print(matching_recipes)
        
        return render_template("search_results.html", matching_recipes=matching_recipes)
        
        
        """
        #checkbox_string = ' '.join(checkboxes)
        print(checkboxes)
        cursor = mongo.db.recipes.find({ "$and": [{ "$text": { "$search": search_text }}, { checkboxes: True}, ] }) 
        matching_recipes = [matching_recipe for matching_recipe in cursor]
        return render_template("search_results.html", matching_recipes=matching_recipes)
        """
        """
        dairy_free = "dairycheck" in request.form.get
        vegan = "vegancheck" in request.form.get
            
        
        print(dairy_free)
        print(vegan)
        
        
        
        #else:
        
        """
        
       
    
"""    
@app.route('/search_results')
def search_results():
    return render_template("search_results.html", recipes=mongo.db.recipes.find())
"""    
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