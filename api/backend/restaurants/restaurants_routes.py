########################################################
# blueprint of endpoints for restaurants
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

restaurants = Blueprint('restaurants', __name__)

@restaurants.route('/menuitems', methods=['GET'])
def get_menu_items():
    current_app.logger.info('restaurant_routes.py: GET /menuitems')

    cursor = db.get_db().cursor()
    cursor.execute('SELECT itemName, restId, price, calories, photo FROM MenuItems WHERE restId = 1;')
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@restaurants.route('/menuitem/<itemName>', methods=['GET'])
def get_menu_item(itemName):
    current_app.logger.info('restaurant_routes.py: GET /menuitems/<itemName>')

    cursor = db.get_db().cursor()
    cursor.execute('SELECT itemName, restId, price, calories, photo FROM MenuItems WHERE restId = 1 AND LCASE(REPLACE(itemName, ' ','')) = {0}'.format(itemName))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Get all restaurants from the DB
@restaurants.route('/restaurants', methods=['GET'])
def get_restaurants():
    current_app.logger.info('restaurant_routes.py: GET /restaurants')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT itemName, restId, price, calories, photo FROM MenuItems WHERE restId = 1;')
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update a menu item
@restaurants.route('/restaurants', methods=['PUT'])
def update_menu_item():
    current_app.logger.info('PUT /restaurants route')
    menu_info = request.json
    # current_app.logger.info(cust_info)
    restId = menu_info['restId']
    itemName = menu_info['itemName']
    price = menu_info['price']
    calories = menu_info['calories']

    query = 'UPDATE MenuItems SET price = %s, calories = %s WHERE restId = %s and itemName = %s'
    data = (restId, itemName, price, calories)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Menu item successfully updated!'
    
