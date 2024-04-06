from flask import Flask, render_template

app = Flask(__name__)  # create an Flask instances


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


# invalid internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
