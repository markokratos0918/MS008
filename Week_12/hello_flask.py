from flask import Flask

app = Flask(__name__)
@app.route('/')
def hello_flask():
    return ("<h1>'Hello, Flask Activity 1!'</h1>")

@app.route("/marko")
def marko():
    return ("<h2>'Marko is Flask!'</<h2>")

@app.route('/cal/<int:number>')
def show_square(number):
    return f"The square of {number} is {number**2}"