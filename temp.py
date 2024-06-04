from flask import Flask, render_template # type: ignore

# Create a flask instance
app = Flask(__name__)


# Create a route decorator
@app.route('/')

def index():
    return "Hello World!!"


# $env:FLASK_ENV="development"     # Set the Flask environment to development (optional)
# $env:FLASK_APP="temp.py"         # Set the Flask app entry point
# flask run


# localhost:5000/user/Vansh
@app.route('/usertemp/<name>')

def usertemp(name):
    return "Hello {}!!".format(name)



# filters that can be used - 
#   safe
#    capitalize
#    lower
#    upper
#    title
#    trim
#    striptags



# Using templates
@app.route('/home')

def home():
    first_name = "Vansh"
    nofilter = "This is <strong>Without Filter text</strong> text."
    safe_use = "This is <strong>Bold</strong> text."
    striptags_use = "This is <strong>Striptags</strong> text."
    
    # Passing list 
    pizzas = ["Cheese", "Pepparoni", "Tomato", 31, 45]
    
    return render_template("index.html", 
            first_name = first_name,
            nofilter = nofilter,
            safe_use = safe_use,
            striptags_use = striptags_use,
            pizzas = pizzas)


@app.route('/user/<name>')

def user(name):
    return render_template("user.html", name=name)


# Create custom error Pages

@app.errorhandler(404)

def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)

def page_not_found(e):
    return render_template("500.html"), 500