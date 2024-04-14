from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired  # 檢查資料是否為空

app = Flask(__name__)  # create a Flask instances
app.config['SECRET_KEY'] = 'flasker'  # set a secret key for the application


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


# create custom error page

# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# invalid internal server error page
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


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


if __name__ == '__main__':
    app.run()
