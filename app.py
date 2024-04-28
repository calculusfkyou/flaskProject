from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired  # 檢查資料是否為空
from flask_sqlalchemy import SQLAlchemy  # 用來操作資料庫
from datetime import datetime  # 用來建立時間紀錄

app = Flask(__name__)  # create a Flask instances
# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 設置資料庫的位置
# secret key
app.config['SECRET_KEY'] = 'flasker'  # set a secret key for the application
# initialize the database
db = SQLAlchemy(app)  # create a database instance

with app.app_context():
    db.create_all()


# create a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # create a string
    def __repr__(self):
        return '<Name %r>' % self.name


# create a user form class
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


# create a form class
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# create a route decorator
@app.route('/')
# put application's code here

# def index():
#     return '<h1>Hello World!</h1>'

def index():
    first_name = 'John'
    favorite_pizza = ['Pepperoni', 'Cheese', 'Mushrooms', 41]

    return render_template('index.html', first_name=first_name,
                           favorite_pizza=favorite_pizza)


# localhost:5000/user/name
@app.route('/user/<name>')
# def user(name):
#     return '<h1>Hello, %s!</h1>' % name

def user(name):
    return render_template('user.html', user_name=name)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User Added Successfully!')

    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)


# create Name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()

    # Validate the form
    if form.validate_on_submit():  # check if the form is submitted
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully!')

    return render_template('name.html', form=form, name=name)


# create custom error page

# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# invalid internal server error page
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
