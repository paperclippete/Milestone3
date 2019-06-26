import os
import json
from flask import Flask, flash, render_template, redirect, request, url_for, session, jsonify
from flask_pymongo import PyMongo, pymongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from forms import user_login_form, user_register_form, user_update_form


app = Flask(__name__)

# Hidden and secure environment variables
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["DBS_NAME"] = os.getenv("DBS_NAME")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user_login'
recipes = mongo.db.recipes


# Flask login class to support secure login/logout and user session
class User:
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @login_manager.user_loader
    def load_user(username):
        site_user = mongo.db.users.find_one({"username": username})
        if not site_user:
            return None
        return User(site_user)


@app.route('/')
@app.route('/index')
def home():
    """ Index page """
    return render_template("index.html", recipes=recipes)


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    """ User login page using WTForm """
    form = user_login_form()
    return render_template("user_login.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login route to get user data from db """
    form = user_login_form()
    users = mongo.db.users
    if request.method == 'GET' and current_user.is_authenticated:
        return json.dumps(current_user.username['first_name'].capitalize())
    if request.method == 'POST':
        the_user = users.find_one({"username": form.username.data.lower()})
        if the_user and User.check_password(the_user["password"], form.password.data):
            user_obj = User(the_user["username"])
            login_user(user_obj)
            return render_template("user_home.html", users=users, user=the_user)
    error = "Invalid password/ username"
    return render_template("user_login.html", error=error, form=form)


@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    """ User register page using WTForm """
    form = user_register_form()
    return render_template("user_register.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Register route will generate hashed password and create new db document """
    users = mongo.db.users
    form = user_register_form()
    existing_user = users.find_one({'username': form.username.data})
    if existing_user is None:
        securepass = generate_password_hash(form.password.data, method="sha256")
        new_doc = {
            'username': form.username.data.lower(),
            'password': securepass,
            'first_name': form.firstname.data.lower(),
            'last_name': form.lastname.data.lower()
        }
        users.insert_one(new_doc)
        flash("Hi " + form.firstname.data.capitalize() +", please login!")
        return redirect(url_for('user_login'))
    error = "That username already exists"
    return render_template("user_register.html", error=error, form=form)


@app.route('/user_home')
@login_required
def user_home():
    """ User home page """
    users = mongo.db.users
    loggeduser = current_user.username["_id"]
    the_user = users.find_one({"_id": loggeduser})
    return render_template("user_home.html", user=the_user, users=users)


@app.route('/logout')
def logout():
    """ User logout route will clear the session """
    logout_user()
    return redirect(url_for('home'))


@app.route('/find_recipes', methods=['GET', 'POST'])
def find_recipes():
    """ Find recipes route from Index page search box and checkboxes """
    users = mongo.db.users
    if request.method == 'POST':
        search_text = request.form.get("search_text")
        checkboxes = request.form.getlist("check")
        print(checkboxes)
        # Search textbox (if empty, else text) with no checkboxes checked
        if len(checkboxes) == 0:
            if search_text == "":
                cursor = mongo.db.recipes.find().sort([("like_count", -1)])
                matching_recipes = [matching_recipe for matching_recipe in cursor]
            else:
                cursor = mongo.db.recipes.find({"$text": {"$search": search_text}}).sort([("like_count", -1)])
                matching_recipes = [matching_recipe for matching_recipe in cursor]
        # Search textbox (if empty, else text) with one checkbox checked        
        elif len(checkboxes) == 1:
            if search_text == "":
                cursor = mongo.db.recipes.find({checkboxes[0]: True})
                matching_recipes = [matching_recipe for matching_recipe in cursor]
            else:
                cursor = mongo.db.recipes.find({"$and": [{"$text": {"$search": search_text}}, {checkboxes[0]: True}]}).sort([("like_count", -1)])
                matching_recipes = [matching_recipe for matching_recipe in cursor]
        # Search textbox (if empty, else text) with two checkboxes checked        
        elif len(checkboxes) == 2:
            if search_text == "":
                cursor = mongo.db.recipes.find({"$and": [{checkboxes[0]: True}, {checkboxes[1]: True}]}).sort([("like_count", -1)])
                matching_recipes = [matching_recipe for matching_recipe in cursor]
            else:
                cursor = mongo.db.recipes.find({"$and": [{"$text": {"$search": search_text}}, {checkboxes[0]: True}, {checkboxes[1]: True}]}).sort([("like_count", -1)]) 
                matching_recipes = [matching_recipe for matching_recipe in cursor]
        # Search textbox (if empty, else text) with three checkboxes checked        
        elif len(checkboxes) == 3:
            if search_text == "":
                cursor = mongo.db.recipes.find({"$and": [{checkboxes[0]: True}, {checkboxes[1]: True}, {checkboxes[2]: True}]}).sort([ ("like_count", -1)])
                matching_recipes = [matching_recipe for matching_recipe in cursor]
            else:
                cursor = mongo.db.recipes.find({"$and": [{"$text": {"$search": search_text}}, {checkboxes[0]: True}, {checkboxes[1]: True}, {checkboxes[2]: True}]}).sort([("like_count", -1)]) 
                matching_recipes = [matching_recipe for matching_recipe in cursor]
        # To enable the user to edit their recipes from the main search page
        if current_user.is_active:
            loggeduser = current_user.username["_id"]
            the_user = users.find_one({"_id": loggeduser})
            return render_template("search_results.html", matching_recipes=matching_recipes, user=the_user)

        return render_template("search_results.html", matching_recipes=matching_recipes)


@app.route('/search_results')
def search_results():
    """ Back Button Fix (temporary) """
    cursor = mongo.db.recipes.find().sort([("like_count", -1)])
    matching_recipes = [matching_recipe for matching_recipe in cursor]
    return render_template("search_results.html", matching_recipes=matching_recipes)


@app.route('/my_account/<user_id>')
@login_required
def edit_account(user_id):
    """ User can view and update their db document """
    users = mongo.db.users
    the_user = users.find_one({"_id": ObjectId(user_id)})
    form = user_update_form()
    return render_template("my_account.html",  user=the_user, users=users, form=form)


@app.route('/update_user/<user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    """ Update user route will update db document """
    users = mongo.db.users
    the_user = users.find_one({"_id": ObjectId(user_id)})
    form = user_update_form()
    securepass = generate_password_hash(form.password.data, method="sha256")
    users.update({'_id': ObjectId(user_id)},
    {
        'first_name': form.firstname.data.lower(),
        'last_name': form.lastname.data.lower(),
        'username': form.username.data.lower(),
        'password': securepass,
    })
    flash("You've updated your details, please login.")
    return render_template("user_login.html", form=form, user=the_user, users=users)    


@app.route('/view_recipe/<recipe_id>', methods=["GET", "POST"])
def view_recipe(recipe_id):
    """ View a recipe from the db """
    the_recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    # Ensure method prints in html with capital letters
    method_string = the_recipe['method']
    method_format = ""
    sentences = list(method_string.split(".")) 
    for i in range(len(sentences)): 
        sentences[i] = sentences[i].strip() 
        sentences[i] = sentences[i][:1].upper() + sentences[i][1:] 
        method_format += sentences[i] + ". " 
    users = mongo.db.users
    if current_user.is_authenticated:
        loggeduser = current_user.username["username"]
        the_user = users.find_one({"username": loggeduser})
        if the_user['_id'] in the_recipe["likes"]:
            user_liked = True
            return render_template("view_recipe.html", recipe=the_recipe, user=the_user, users=users, method_format=method_format, user_liked=user_liked)
        return render_template("view_recipe.html", recipe=the_recipe, user=the_user, users=users, method_format=method_format)
    return render_template("view_recipe.html", recipe=the_recipe, method_format=method_format)
    

@app.route('/add_recipe', methods=['GET','POST'])
@login_required
def add_recipe():
    """ Add a new recipe to the db """
    users = mongo.db.users
    loggeduser = current_user.username["username"]
    the_user = users.find_one({"username": loggeduser})
    return render_template("add_recipe.html", the_user=the_user, recipes=recipes)


@app.route('/insert_recipe', methods=['POST'])    
@login_required
def insert_recipe():
    """ Insert recipe route will insert a new recipe document into the db """
    ingredient_list = request.form.getlist("ingredient")
    amount_list = request.form.getlist("amount")
    ingam_dict = dict(zip(ingredient_list, amount_list))
    vegan = request.form.get("vegan")
    dairyfree = request.form.get("dairyfree")
    glutenfree = request.form.get("glutenfree")
    new_doc = {
            'title': request.form.get('title').lower(),
            'author': request.form.get('author').lower(),
            'image': request.form.get('img_url'),
            'main_ingredient': request.form.get('main_ingredient'),
            'recipe_description': request.form.get('recipe_description'),
            'ingredients': ingam_dict,
            'method': request.form.get('method'),
            'vegan': bool(vegan),
            'dairy_free': bool(dairyfree),
            'gluten_free': bool(glutenfree),
            'prep_time': request.form.get('prep_time'),
            'serves': request.form.get('serves'),
            'likes': []
        }
    recipes.insert_one(new_doc)
    flash("You have added a new recipe.")
    return redirect(url_for("user_home"))


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    """ User can edit recipe details, view will be pre-populated with current db info """
    the_recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    users = mongo.db.users
    loggeduser = current_user.username["username"]
    the_user = users.find_one({"username": loggeduser})
    return render_template("edit_recipe.html", the_user=the_user, recipe=the_recipe, recipes=recipes)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
@login_required
def update_recipe(recipe_id):
    """ Update recipe route will post updated document to the db """
    ingredient_list = request.form.getlist("ingredient")
    amount_list = request.form.getlist("amount")
    ingam_dict = dict(zip(ingredient_list, amount_list))
    vegan = request.form.get("vegan")
    dairyfree = request.form.get("dairyfree")
    glutenfree = request.form.get("glutenfree")
    recipes.update({'_id': ObjectId(recipe_id)},
        {
            'title': request.form.get('title').lower(), 
            'author': request.form.get('author').lower(),
            'image': request.form.get('img_url'),
            'main_ingredient': request.form.get('main_ingredient'),
            'recipe_description': request.form.get('recipe_description'),
            'ingredients': ingam_dict,
            'method': request.form.get('method'),
            'vegan': bool(vegan),
            'dairy_free': bool(dairyfree),
            'gluten_free': bool(glutenfree),
            'prep_time': request.form.get('prep_time'),
            'serves': request.form.get('serves')
        })
    flash("You have updated this recipe.")
    return redirect(url_for("user_home"))


@app.route('/delete_recipe/<recipe_id>', methods=["GET", "POST"])
@login_required
def delete_recipe(recipe_id):
    """ User can delete their own recipes from the db """
    recipes.remove({'_id': ObjectId(recipe_id)})
    flash("You have deleted this recipe.")
    return redirect(url_for("user_home"))


@app.route('/my_recipes/<user_id>')    
@login_required
def my_recipes(user_id):
    """ User can view all of the recipes they have created """
    users = mongo.db.users
    loggeduser = current_user.username["username"]
    print(loggeduser)
    the_user = users.find_one({"username": loggeduser})
    print(the_user)
    cursor = mongo.db.recipes.find({"author": the_user['username']}).sort([("like_count", -1)])
    matching_recipes = [matching_recipe for matching_recipe in cursor]
    return render_template("search_results.html", matching_recipes=matching_recipes, user=the_user)


@app.route('/liked_recipes/<user_id>')    
@login_required
def liked_recipes(user_id):
    """ User can view all of the recipes they have liked """
    users = mongo.db.users
    the_user = users.find_one({"_id": ObjectId(user_id)})
    cursor = mongo.db.recipes.find({"likes": the_user['_id']}).sort([("like_count", -1)])
    matching_recipes = [matching_recipe for matching_recipe in cursor]
    return render_template("search_results.html", matching_recipes=matching_recipes, user=the_user)


@app.route('/like_recipe/<recipe_id>/<user_id>', methods=["GET", "POST"])
def like_recipe(recipe_id, user_id):
    """ Like a recipe will increase a recipes like count and log the user_id to an array in the db """
    users = mongo.db.users
    loggeduser = current_user.username["_id"]
    the_user = users.find_one({"_id": loggeduser})
    the_recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    recipes.update({'_id': ObjectId(recipe_id), 
                    "likes": {"$ne": ObjectId(loggeduser)}},
                   {"$inc": {"like_count": 1}, 
                     "$push": {"likes": ObjectId(loggeduser)}})
    method_string = the_recipe['method']
    method_format = ""
    sentences = list(method_string.split(".")) 
    for i in range(len(sentences)): 
        sentences[i] = sentences[i].strip() 
        sentences[i] = sentences[i][:1].upper() + sentences[i][1:] 
        method_format += sentences[i] + ". "
    #user_liked = True
    return render_template("view_recipe.html", recipe=the_recipe, user=the_user, method_format=method_format, user_liked=user_liked)
   

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
