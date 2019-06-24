# Dessert ![Cake](static/img/cake1.png=40x40) Finder

Welcome to Dessert Finder. 

This is a web application that allows users to store and access dessert recipes. There is a robust non-relational database schema hosted on MongoDB. A backend code that groups and summarises the recipes on the site, based on their attributes and a frontend page to show this summary, and make the categories clickable to drill down into a filtered view based on that category. Using Python and Flask the backend code will retrieve a list of recipes, filtered based on various criteria (e.g. allergens, cuisine, etc…) and order them based on some reasonable aspect (e.g. number of views or upvotes). The frontend page will display these and show some summary statistics for the data.
There is a detailed view for each recipe, that would just show all attributes for that recipe, and the full preparation instructions. Users can edit and delete their own recipe records as well as their user details.
There is a secure user registration and authentication to the site. This allows for a more personalised experience and ensures data is secure.

View the deployed site [here](https://dessert-search-ms3ag.herokuapp.com/index)

| Contents  |
|-----------|
|[UX](#UX) |
|[Features](#Features)|
|[Testing](#Testing)|
|[Deployment](#Deployment)|
|[Credits](#Credits)|

### UX
___

#### Strategy

The site should...

* be visually appealing - using colours, styles and fonts which reflects the style of the brand
* provide quick access to the database of recipes
* allow the user to search for recipes by ingredient and allergen information
* allow the user to filter their search results
* allow users to add/delete and change recipes in the database
* allow users to add/change their details in the database
* allow users to like and save recipes

For the user the site should...

* be intuitive and easy to use
* be personalised and welcoming
* provide quick access to recipes with a very simple search and filter function
* look appealing and in keeping with the brand
* ensure their data is secure
* allow them to manage their own recipes and user data
* allow them to keep their favourite(liked) recipes


##### User Stories

* As an inexperienced cook... 
    1. I want quick access to a variety of desserts based on ingredients I know I like
    2. I want to be able to find recipes that are quick to make
    3. I want to be able to save the recipes that I have enjoyed
* As an experienced cook...
    1. I want quick access to a variety of desserts based on ingredients I like
    2. I want to see information about the recipe (such as preparation time, how many it serves and allergen information) at a glance
    3. I want to be able to share my knowledge and experience by easily adding my own recipes to the site
    4. I want to be able to manage my recipes, editing them or deleting them as necessary
    5. I want to be able to save my favourite recipes and access them quickly
* As a user with food-intolerance or allergies...
    1. I want to search a database of recipes that will be suitable to my needs
    2. I want to clearly see suitable recipes at a glance

#### Scope

In order to create a good UX Dessert Search...

* be developed with a mobile-first approach in order to suit the target user group (cooks using phones or tablets in the kitchen)
* be responsive in order to display across a range of devices
* be intuitive and provide feedback to the user on their actions
* should feature a cohesive design which promotes the Dessert Search brand
* will have a simple search interface with filters
* will be functional to any user, whether logged in or not, but provide extra functionality and personalisation to registered users

Please find my initial wireframe and database schema, created using Balsamiq, [here](development/DessertSearch.pdf)

![Cake 2](static/img/cake2.png=40x40)

### Features
___

#### Existing Features

> Navigation Bar/ Dropdown Menu

I used Bootstrap 4 to create a minimalist navigation bar that would toggle a dropdown menu on mobile/tablet devices. A user should not have to use the browser's back-button as the navigation bar is fixed. 

> Hero Video

I set the body element a fixed background video on larger devices as it creates a modern/ professional touch and adds credibility to the site. As it wouldn't render correctly on mobile devices I opted for a background image with an overlay which would help with text-contrast and readability.

> Main Search Box

For good UX design I decided to have a minimal search interface on the index page. I used Python to programme how this would search the database and created a very complex code of if statements to try and predict how users would use this. Pressing search without entering text or checking a checkbox will show the whole database, I felt this was required to meet the needs of users who were unsure what they were looking for. I have also used Jinja templating to add a button to return to the search page if 0 recipes are found.

> Filter Checkboxes

Again, for good UX design in keeping with a minimal search interface on the index page I used checkboxes to filter the database results before they displayed. This was by far one of the most difficult functions of my design and took a long time to code, debug and eventually implement. I have written a very complex function using Python to ensure that everything works as intended for the user.

> Filter Accordion on Search Results

I felt that some users may not be sure what they are looking for immediately, having extra filters on the search results page would prevent users from having to navigate back to the search box. I used jQuery to hide recipe cards that did not match the checked checkboxes and created a button that would reset the filters. It was important that for each additional checkbox that was checked the recipes would be filtered further and not reset.

> Bootstrap 4 grid layout and cards

I used Bootstrap styling for my search results and user home pages to ensure that the pages would be as responsive as possible. I also used cards for a standard layout of recipes, this is visually effective because it porvides the necessary 'at-a-glance' details for the user. I also used "object-fit:cover" in CSS to try to ensure that each recipe image would display nicely within the card.

> User Register and Login using WTForms and Werkzeug security

I imported Flask WTForms and Werzkeug Security to create a login process that was secure and created user profiles in my database. It ensured there were no duplicate usernames and that recipe author and recipe likes could be found and personalised for each registered user.

> Fetch API

I used Fetch to 'GET' user data from my Python app.py, this ensured that the user would only see menu links that were appropriate to them i.e. non-registered users would see login and sign up links but current authenticated users would be able to access their user home.

> Jinja Templating

I used Jinja templating to create a base.html page with navbar and footer that would ensure a standardised aesthetic across the site. I also used the templating to print data from the database (i.e. within 'edit recipe' the previous input is displayed in the form) and create if and for loops that continued to personalise the user's experience.

#### Features for the Future

It would be appropriate to obtain mailing data from the user in order to have a mailing list with new and featured recipes.

It would be highly likely that pagination would be required as the database grows.

It would be suitable to find a way for users to upload their own photographs of the recipes rather than entering a URL.

It could be possible to allow users to comment on recipes, creating more of a community ethos.

It could be possible to integrate social media feeds (i.e. Instagram) to provide more user-generated content and community.

#### Technologies Used

* **HTML** - used for creating content and basic layout and validated with W3C
* **CSS** - used for customised styling and layout and validated with W3C
* **JavaScript** - used to provide interactivity and logic to the site
* [Python](https://www.python.org/) - used to programme the site and interact between the database and the frontend
* [Flask](http://flask.pocoo.org/) - A Python micro framework that includes [Jinja Templating](http://jinja.pocoo.org/) and [Werzkeug](https://werkzeug.palletsprojects.com/en/0.15.x/) debugger. Werzkeug also provided password hashing which would ensure users' passwords are encrypted before being stored in the database.
* [PyMongo](https://api.mongodb.com/python/current/) - An API which provides tools for working with MongoDB in Python
* [MongoDB](https://www.mongodb.com/) - non-relational document style database used to store the recipes and users for Dessert Search
* [WTForms](https://wtforms.readthedocs.io/en/stable/) - An API which provides form classes for ease of managing form data in Python
* [Cloud9 IDE](https://ide.c9.io/) - this was the IDE where I developed and ran my application
* **Git** - I pushed my files using **Git**, storing them in a repository on **GitHub**
* [Heroku](https://heroku.com/) - I deployed my finished site through Heroku
* [jQuery](https://jquery.com/) - JavaScript library used to connect with APIs and custom-code for the site which allows for DOM manipulation
* [SASS](https://sass-lang.com/) - used as a preprocessor in creating style files with variables, media queries and mixins
* [CSS Minifier](https://cssminifier.com/) - used to minify my CSS data for deployment
* [Bootstrap 4](https://getbootstrap.com/) - used for responsive layout, basic styling, dropdown Navbar (JavaScript for these features was used - linked to Bootstrap 4 and, through BS4, popper.js in <script> tags)
* [Google Fonts](https://fonts.google.com/) - used for customised fonts
* [Font Awesome 5](https://fontawesome.com/) - used for links and icons to make the site more appealing
* [Favicon Generator](https://www.favicon.cc/?) - I used this to generate a Favicon
* [W3C Validator](https://validator.w3.org/) - HTML Validator, [W3C CSS Validator](https://jigsaw.w3.org/css-validator/), [Esprima](esprima.org) - JS Validator
* Chrome Developer Tools, Stack-Overflow, Code-Institue Slack Community, Code-Institute module notes, W3Schools, CSS Tricks, Pretty Printed YouTube videos - all used for reference when I encountered a bug or required extra support with any issues.

### Testing
___

#### Manual and Automated Testing

Manual testing was done for all CRUD operations from the database as well as for all links, buttons and forms in the site. I used Werkzeug Debugger throughout the development process to immediately flag errors when running my app.py file.

I created a [test.py](development/testing/testdb.py) file that tested the connection to my database, ensuring data was inserted in a suitable manner and was returned to the console when requested.

Throughout the process I continually manually tested the frontend, by saving my work in the IDE and running it in Google Chrome. I used Chrome Developer Tools to ensure that my site was responsive and functioned in all screen sizes and that my styling was applied appropriately throughout. 

I set ```console.logs``` and ```debugger``` statements throughout my js files in order to debug through the console.

I used jQuery to manipulate the DOM in Chrome Developer Tools in order to test my code visually before writing it within the script.

I had several users log in and out of the website searching, adding, editing and deleting (CRUD) the recipes. This was to ensure that only registered users were able to delete/edit their own recipes. It also verified that the correct author showed up for each recipe. 

#### Responsiveness

I tested my project throughout development using Chrome Developer Tools to check the site was responsive. I continually made adjustments to my media-queries in CSS to ensure it looked good at all screen-widths, however I realised my laptop had a different screen size to the standard. I began to investigate a range of screen sizes and realised the best option was just to make it as responsive as I possibly could!

#### Bugs

There were several issues with my Python code, however, using the Werkzeug Debugger allowed for an immediate fix. I used the documentation for Flask, PyMongo and MongoDB to help solve any problems. I found it very difficult to get a search function that would search text and use checkboxes. I eventually had code that would work in every instance although I am aware that it could be neater.

There was a 500 error displaying in the console when Fetch was trying to retrieve login details from an anonymous user. I've run out of time on my project to fix this issue but I'd look into an if statement in the fetch function or in python to catch this.

There was a 400 error in the console for the favicon. I created a favicon.

There have been several issues throughout development with my JS code breaking, I worked hard using console.logs and debuggers to pinpoint errors and fix them. There shouldn't be any errors displaying in the console.

When a user liked a recipe and then clicked the back button it took them back to view recipe with an active like recipe button again. I fixed this by searching the current url for 'like_recipe', if it was located the back button would go back by 2 pages.

There was a security issue related to the app.py view where the database string was returned in the URL. This could enable people to find and access the dtabase. I quickly fixed the URL parameter to be the user._id rather than users._id.

### Deployment
___

I saved my work regularly on the IDE Cloud 9. I also committed my code to GitHub at regular intervals. I feel that I am now using git more often, making sure to give detailed commit messages as I know it provides version control.

In order to deploy my work I opened the terminal within Cloud 9...

* initialised and set up a local git repository with the command ``` git init ```

* added files to my git repo with the command ``` git add (specific file location or . for all files) ```

* commited files to the local repo with ``` git commit``` and wrote a message after -m that would be useful in either complex projects or when working collaboratively.

* in order to commit my code to a remote repository I had to create a new project on GitHub and then typed into the terminal ``` git remote add origin``` followed by ``` https://github.com/[USER NAME]/[PROJECT NAME]```

* I then used ``` git push -u origin master``` to push my code to my master branch as I was only using one branch. I did not feel that my project was complex enough to create another branch, however I did spend time familiarising myself with this.

* Each time after initial commit I would use ``` git push``` to push my code to Git Hub

* In GitHub I then published my master branch to GitHub pages, this is my deployed version. 

* In order to deploy the site to Heroku, I had to create a Procfile and requirements.txt. To create a Procfile - ```echo web: python (your filename).py > Procfile ``` To create a requirements.txt - ```sudo pip3 freeze --local > requirements.txt ``` These will tell Heroku how to run your app.

* Next, I logged into Heroku ``` $ heroku login ``` and set up the remote ``` git remote add heroku(url) ```, I then deployed to Heroku using ``` git push heroku master```

* I then navigated to the Heroku website where I had to set up the config vars. The IP is 0.0.0.0 and the PORT is 8080. I also included my MONGO_URI, DB_NAME and SECRET KEY. These were saved as environment variables in Cloud 9 and had to be entered manually into Heroku to avoid commiting them to GIT.

* If you're interested in cloning this repository, to set up and install everything in the requirements.txt run the following command in the terminal:

```$ sudo pip3 -r install requirements.txt```

* Please note that I used Cloud9 for this project, so if you are using a different editor, the terminal commands may differ. Also you will have to create your own Database and Secret Keys. These values are kept secret in order to provide security to users.

**The difference between the deployed version and the development version is that I'm using a minified CSS file whereas I used SASS to compile my styling during development. I also set the debug to false for deployment.**

### Credits
___

#### Content
The recipes and recipe images were inserted for testing purposes were taken from the BBC website.

The background image was from Pexels, the video was from Videvo. The cake images and icons were from FlatIcon.

**This site has been created for educational purposes only**

#### Media
The images displayed in this site were either my own or sourced from the sites listed above. All images are for educational purposes only.




