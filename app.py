import os
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["DBS_NAME"] = os.getenv("DBS_NAME")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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
    def load_user(self, username):
        site_user = mongo.db.users.find_one({"username": username})
        if not site_user:
            return None
        return User(site_user["username"])


recipes = mongo.db.recipes


@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html", recipes=recipes)
    
    
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    return render_template("user_login.html")
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    users=mongo.db.users
    the_user = users.find_one({'username': request.form.get('username')})
    password = request.form.get('password')
    if the_user and User.check_password(the_user["password"], password):
            user_obj = User(the_user["username"])
            login_user(user_obj)
            return render_template("user_home.html", users=users)
    error = "Invalid password/ username"
    return render_template("user_login.html", error=error)

@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    return render_template("user_register.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    users = mongo.db.users
    existing_user = users.find_one({'username': request.form.get('username')})
    if existing_user is None:
        securepass = generate_password_hash(request.form["password"], method="sha256")
        new_doc = {
            'username' : request.form.get('username'), 
            'password' : securepass, 
            'first_name' : request.form.get('firstname'), 
            'last_name' : request.form.get('lastname')
        }
        users.insert_one(new_doc)
        session['username'] = request.form.get('username')
        return redirect(url_for('user_home'))  
    error = "That username already exists"
    return render_template("user_register.html", error=error)
    
@app.route('/user_home')
def user_home():
    users = mongo.db.users
    return render_template("user_home.html", users=users)  
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    
@app.route('/find_recipes', methods=['POST'])
def find_recipes():
    if request.method == 'POST':
        search_text = request.form.get("search_text")
        checkboxes = request.form.getlist("check")
        print(checkboxes)
        #search text with checkboxes 
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

@app.route('/my_account/<user_id>')       
def edit_account(user_id):
    users = mongo.db.users
    the_user = users.find_one({"_id": ObjectId(user_id)})
    return render_template("my_account.html", users=users, user=the_user)

@app.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    users = mongo.db.users
    securepass = generate_password_hash(request.form["password"], method="sha256")
    users.update({'_id': ObjectId(user_id)},
    {
        'first_name':request.form.get('firstname'),
        'last_name':request.form.get('lastname'),
        'username': request.form.get('username'),
        'password': securepass,
    })
    message = "You've updated your details"
    return render_template("user_home.html", message=message)    

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