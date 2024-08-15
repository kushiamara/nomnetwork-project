########################################################
# blueprint of endpoints for restaurants
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

restaurants = Blueprint('restaurants', __name__)

# menuitems GET route to return all menu items
@restaurants.route('/restaurants/menuitems/<restId>', methods=['GET'])
def get_menu_items(restId):
    current_app.logger.info('restaurant_routes.py: GET /menuitems/<restId>')

    cursor = db.get_db().cursor()
    cursor.execute('SELECT itemName, restId, price, calories, photo FROM MenuItems WHERE restId = {0};'.format(restId))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# menuitems POST route to add a menu item
@restaurants.route('/restaurants/menuitems', methods=['POST'])
def add_menu_item():
    # collecting data from the request object 
    the_data = request.json
    # return the_data
    current_app.logger.info(the_data)
    # extracting the variable
    itemName = the_data['itemName']
    restId = the_data['restId']
    price = the_data['price']
    calories = the_data['calories']
    photo = the_data['photo']
    # return {"query":"test"}
    # Constructing the query
    sql = '''INSERT into MenuItems (itemName, restId, price, calories, photo) values ('{0}', {1}, {2}, {3}, '{4}')'''.format(itemName, restId, price, calories, photo)
    current_app.logger.info(sql)
    # return {"query":sql}
    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    db.get_db().commit()
    return {"result": 'You have successfully added a menu item!'}

# menuitem GET route to return a specific menu item given its name
@restaurants.route('/restaurants/menuitem/<restId>/<itemName>', methods=['GET'])
def get_menu_item(restId, itemName):
    current_app.logger.info('restaurant_routes.py: GET /menuitems/<restId>/<itemName>')

    cursor = db.get_db().cursor()
    cursor.execute("SELECT itemName, restId, price, calories, photo FROM MenuItems WHERE restId = {0} AND LCASE(REPLACE(itemName, ' ','')) = '{1}'".format(restId, str(itemName).casefold()))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# menuitem PUT route to update a menu item
@restaurants.route('/restaurants/menuitem/<restId>/<itemName>', methods=['PUT'])
def update_menu_item(restId, itemName):
    current_app.logger.info('restaurant_routes.py: PUT /menuitems/<restId>/<itemName>')
    # collecting data from the request object 
    the_data = request.json
    # return the_data
    current_app.logger.info(the_data)
    # extracting the variable
    name = the_data['itemName']
    price = the_data['price']
    calories = the_data['calories']
    photo = the_data['photo']

    cursor = db.get_db().cursor()
    cursor.execute("UPDATE MenuItems SET itemName = '{0}', price = {1}, calories = {2}, photo = '{3}' WHERE restId = {4} AND LCASE(REPLACE(itemName, ' ','')) = '{5}'".format(name, price, calories, photo, restId, str(itemName).casefold()))
    db.get_db().commit()
    return 'Item updated!'

# menuitem DELETE route to delete a menu item
@restaurants.route('/restaurants/menuitem/<restId>/<itemName>', methods=['DELETE'])
def delete_menu_item(restId, itemName):  
    current_app.logger.info('restaurant_routes.py: DELETE /menuitems/<restId>/<itemName>')

    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM MenuItems WHERE restId = {0} AND LCASE(REPLACE(itemName, ' ','')) = '{1}'".format(restId, str(itemName).casefold()))
    db.get_db().commit()

    return 'Item deleted'

# tags GET method to return all the restaurants tags
@restaurants.route('/restaurants/tags/<restId>', methods=['GET'])
def get_tags(restId):
    current_app.logger.info('restaurant_routes.py: GET /tags/<restId>')

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT tagName FROM Restaurants
                    LEFT JOIN RestaurantTags ON Restaurants.restId = RestaurantTags.restId
                    JOIN Tags ON RestaurantTags.tagId = Tags.tagId
                    WHERE Restaurants.restId = {0};'''.format(restId))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# # Get all restaurants from the DB
# @restaurants.route('/restaurants', methods=['GET'])
# def get_restaurants():
#     current_app.logger.info('restaurant_routes.py: GET /restaurants')
#     cursor = db.get_db().cursor()
#     cursor.execute('SELECT itemName, restId, price, calories, photo FROM MenuItems WHERE restId = 1;')
#     # row_headers = [x[0] for x in cursor.description]
#     # json_data = []
#     theData = cursor.fetchall()
#     # for row in theData:
#     #     json_data.append(dict(zip(row_headers, row)))
#     the_response = make_response(theData)
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response

# # Update a menu item
# @restaurants.route('/restaurants/<newItem>', methods=['PUT'])
# def update_menu_item():
#     current_app.logger.info('PUT /restaurants route')
#     menu_info = request.json
#     # current_app.logger.info(cust_info)
#     restId = menu_info['restId']
#     itemName = menu_info['itemName']
#     price = menu_info['price']
#     calories = menu_info['calories']

#     query = 'UPDATE MenuItems SET price = %s, calories = %s WHERE restId = %s and itemName = %s'
#     data = (restId, itemName, price, calories)
#     cursor = db.get_db().cursor()
#     r = cursor.execute(query, data)
#     db.get_db().commit()
#     return 'Menu item successfully updated!'
    
