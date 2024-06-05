from flask import Flask, render_template, flash, request # type: ignore
from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, SubmitField # type: ignore
from wtforms.validators import DataRequired # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_migrate import Migrate
from datetime import datetime

# Create a flask instance
app = Flask(__name__)



# Adding Database

# SQLite DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:vvvansh1999%40@localhost/fl_users'

# created a file "create_db.py" and run it to make mysql database


# Secret Key
app.config['SECRET_KEY'] = 'my key'
# Initialize DB
db = SQLAlchemy(app)
# Migration
migrate = Migrate(app, db)



# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


class UserForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")
    
    
@app.route('/user/add', methods=['GET', 'POST'])

def add_user():
    name = None
    form = UserForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name = form.name.data, 
                        email = form.email.data, 
                        favorite_color = form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash("User Added Successfully!!")
    our_users = Users.query.order_by(Users.date_added)
    
    return render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)
    
    

# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])

def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                    form = form,
                    name_to_update = name_to_update,
                    id = id
                    )
        except:
            flash("Error!!!")
            return render_template("update.html",
                    form = form,
                    name_to_update = name_to_update
                    )
    else:
        return render_template("update.html",
                form = form,
                name_to_update = name_to_update,
                    id = id
                )



# Delete Database Record
@app.route('/delete/<int:id>', methods=['GET', 'POST'])

def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!")
        our_users = Users.query.order_by(Users.date_added)

        return render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)
        
    except:
        flash("There's a problem in deleting this User!!")
        return render_template('add_user.html',
            form=form,
            name=name,
            our_users=our_users)

    
# Create a form class
app.config['SECRET_KEY'] = "my key"

class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

## Fields for forms

# BooleanField DateField DateTimeField DecimalField FileField HiddenField MultipleField
# MultipleField FloatField FormField IntegerField PasswordField RadioField SelectField 
# SelectMultipleField TextAreaField


## Validators

# DataRequired Email EqualTo InputRequired IPAddress Length MacAddress NumberRange
# Optional Regex URL UUID AnyOf NoneOf

@app.route('/name', methods=['GET', 'POST'])

def name():
    name = None
    form = NameForm()
    
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!!")
        
    return render_template("name.html", 
            name=name, 
            form=form)
    
    

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



