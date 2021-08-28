#flask is a web framework for python allowing us to act as a server
#second most popular, with the most popular being Django

from flask import Flask, render_template, abort, request
import json

from pymongo import cursor
from data import data
from flask_cors import CORS
from config import db, parse_json

app = Flask(__name__) # create a flask app
CORS(app)


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
    cursor = db.products.find({})
    prods = []
    for prod in cursor:
        prods.append(prod)

    #prods = [ prod for prod in cursor ] 
    return parse_json(prods)


#get post request and save to data

@app.route('/api/catalog', methods=['POST'])
def save_product():
    product = request.get_json() #gets the dictionary 
    #validations
    if not "title" in product:
        return parse_json({"error":"Title is required", "success":False })
    
    if not "price" in product or not product["price"] > 0:
        return parse_json({"error":"positive price is required", "success":False })
    
    if not product["category"]:
        return parse_json({"error":"category is required", "success":False })

    db.products.insert_one(product)
    return parse_json(product)



@app.route("/api/categories")
def get_categories():
    #did it on front end by using for loop, now on back end
    cursor = db.products.find({})
    results = []
    for item in cursor:
        cat = item["category"]

        if cat not in results:
            results.append(cat)
    
    return parse_json(results)

# get a product by its ID
@app.route("/api/catalog/id/<id>") # URL Parameters, whatever is in the URL gets sent as the param in the function
def get_product_by_id(id):
    #return ("Getting by " + id)
    for item in data:
        if(str(item["_id"]) == id):
            return parse_json(item)
    abort(404)

# get all the products belonging to category
@app.route("/api/catalog/category/<cat>")
def get_product_by_category(cat):
    cursor = db.products.find({ "category" : cat })
    results = [prod for prod in cursor]
    return parse_json(results)

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
    return parse_json(results)

@app.route("/api/test/populatedb")
def populate_db():
        for prod in data:
            db.products.insert_one(prod)

        return "Data Loaded"


##
#   DISCOUNT CODES
##

@app.route("/api/coupons")
def get_coupon_codes():
    cursor = db.couponcodes.find({})
    results = [codes for codes in cursor]
    return parse_json(results)

@app.route("/api/coupons", methods=['POST'])
def create_coupon_code():
    code = request.get_json() #gets the dictionary 
    #validations
    if not "_id" in code:
        return parse_json({"error":"specify item by _id", "success":False })
    
    if not "discount" in code or not code["discount"] > 0:
        return parse_json({"error":"positive discount '%' is required", "success":False })

    db.couponcodes.insert_one(code)
    return parse_json(code)

@app.route("/api/coupons/search/<id>")
def coupon_search(id):
    cursor = db.couponcodes.find({ "_id" : id }) #lists codes for all products with this ID
    results = [prod for prod in cursor]
    return parse_json(results)

if __name__ == '__main__':
    app.run(debug=True)


#
#   coupon codes
#   db.couponcodes
#   code, discount
#
#   create a GET to read all
#   create a POST to add discount codes
#   create a GET to search by code, exists and discount > 0
#
#
