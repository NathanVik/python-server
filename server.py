#flask is a web framework for python allowing us to act as a server
#second most popular, with the most popular being Django

from flask import Flask, render_template, abort, request
import json

from pymongo import cursor, results
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
    product = db.products.find_one({"_id": id})
    if not product:
        abort(404)
    return parse_json(product)


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
    if not "code" in code:
        return parse_json({"error":"specify item code", "success":False })
    
    if not "discount" in code or not code["discount"] > 0:
        return parse_json({"error":"positive discount '%' is required", "success":False })

    db.couponcodes.insert_one(code)
    return parse_json(code)

@app.route("/api/coupons/search/<code>")
def coupon_search(code):
    cursor = db.couponcodes.find_one({ "code" : code }) #lists codes for all products with this ID
    return parse_json(cursor)


#
## ORDERS
#

#Post Order
@app.route("/api/orders", methods=['POST'])
def create_order():
    new_order = request.get_json()
# validate at least 1 product
    prods = new_order["cart"]
    count = len(prods)
    if(count < 1):
        abort(400, "Orders without products are not allowed!")

    db.orders.insert_one(new_order)
    return parse_json(new_order)

#get all orders
@app.route("/api/orders")
def get_all_orders():
    cursor = db.orders.find({})
    results = [orders for orders in cursor]
    return parse_json(results)

@app.route("/api/orders/<userID>")
def get_ID_orders(userID):
    cursor = db.orders.find({ "userID" : userID }) 
    results = [orders for orders in cursor]
    return parse_json(results)


if __name__ == '__main__':
    app.run(debug=True)


#
#   Order:
#   post order
#   get all orders
#   get orders by userID
#
#
#
#
#