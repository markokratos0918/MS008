from flask import Flask

app = Flask(__name__)
@app.route('/')
def hello_flask():
    return ("<h1>'Hello, Flask Activity 1!'</h1>")

@app.route("/marko")
def marko():
    return ("<h2>'Marko is Flask!'</<h2>")