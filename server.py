#flask is a web framework for python allowing us to act as a server
#second most popular, with the most popular being Django

import re
from flask import Flask, render_template
import json
from data import data

app = Flask(__name__) # create a flask app

me = {
    "name": "Nathan",
    "last_name": "Vik",
    "age": 32,
    "address": {
        "street": "Reef Ct",
        "number": 1234
    },
    "email": "nathan.t.vik@gmail.com"

}




#HTML Routing

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("index.html")

@app.route('/about')
def about():
    return me

@app.route('/about/me')
def about_me():
    return me['name']

@app.route('/about/fullname')
def fullname():
    return me['name'] + ' ' + me['last_name']

@app.route('/about/email')
def email():
    return me["email"]




#API routing

@app.route('/api/catalog')
def get_catalog():
    return json.dumps(data)

@app.route("/api/categories")
def get_categories():
    #did it on front end by using for loop, now on back end
    results = []
    for item in data:
        cat = item["category"]

        if cat not in results:
            results.append(cat)
    
    return json.dumps(results)





if __name__ == '__main__':
    app.run(debug=True)