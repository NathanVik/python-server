#flask is a web framework for python allowing us to act as a server
#second most popular, with the most popular being Django

import re
from flask import Flask, render_template, abort, request
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

#get post request and save to data

@app.route('/api/catalog', methods=['POST'])
def save_product():
    product = request.get_json() #gets the dictionary 
    data.append(product)

    return json.dumps(product)



@app.route("/api/categories")
def get_categories():
    #did it on front end by using for loop, now on back end
    results = []
    for item in data:
        cat = item["category"]

        if cat not in results:
            results.append(cat)
    
    return json.dumps(results)

# get a product by its ID
@app.route("/api/catalog/id/<id>") # URL Parameters, whatever is in the URL gets sent as the param in the function
def get_product_by_id(id):
    #return ("Getting by " + id)
    for item in data:
        if(str(item["_id"]) == id):
            return json.dumps(item)
    abort(404)

# get all the products belonging to category
@app.route("/api/catalog/category/<cat>")
def get_product_by_category(cat):
    results = []
    for item in data:
        if item["category"].lower() == cat.lower():
            results.append(item)
    return json.dumps(results)

@app.route("/api/catalog/cheapest")
def get_product_cheapest():
    cheapest = data[0]      # set cheapest to first item
    for item in data:
        if item["price"] < cheapest["price"]:       #compare prices, replace if cheaper
            cheapest = item
    results = []
    for item in data:
        if item["price"] == cheapest["price"]:      #add all of lowest price to list
            results.append(item)
    return json.dumps(results)


if __name__ == '__main__':
    app.run(debug=True)