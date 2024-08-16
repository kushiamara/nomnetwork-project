########################################################
# blueprint of endpoints for restaurants
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

restaurants = Blueprint('restaurants', __name__)

# menuitems GET route to return all menu items
@restaurants.route('/restaurants/menuitems/<restId>', methods=['GET'])
def get_menu_items(restId):
    current_app.logger.info('restaurant_routes.py: GET /menuitems/<restId>')

    cursor = db.get_db().cursor()
    cursor.execute('SELECT itemName, price, calories, photo FROM MenuItems WHERE restId = {0};'.format(restId))
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
    cursor.execute("UPDATE MenuItems SET itemName = '{0}', price = {1}, calories = {2}, photo = '{3}' WHERE restId = {4} AND itemName = '{5}' ".format(name, price, calories, photo, restId, itemName))
    db.get_db().commit()
    return 'Item Updated!'

# menuitem DELETE route to delete a menu item
@restaurants.route('/restaurants/menuitem/<restId>/<itemName>', methods=['DELETE'])
def delete_menu_item(restId, itemName):  
    current_app.logger.info('restaurant_routes.py: DELETE /menuitems/<restId>/<itemName>')

    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM MenuItems WHERE restId = {0} AND itemName = '{1}' ".format(restId, itemName))
    db.get_db().commit()

    return 'Item Deleted'

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

# tags GET method to return all tags existing in the Tags table
@restaurants.route('/restaurants/gettags', methods=['GET'])
def find_all_tags():
    sql = '''SELECT tagName, tagId FROM Tags'''
    current_app.logger.info('GET /restaurants/gettags route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# tag POST route to add a tag to the restaurant
@restaurants.route('/restaurants/tags', methods=['POST'])
def add_tag():
    # collecting data from the request object 
    the_data = request.json
    # return the_data
    current_app.logger.info(the_data)
    # extracting the variable
    restId = the_data['restId']
    tagId = the_data['tagId']
    # return {"query":"test"}
    # Constructing the query
    sql = '''INSERT into RestaurantTags (tagId, restId) values ({0}, {1})'''.format(tagId, restId)
    current_app.logger.info(sql)
    # return {"query":sql}
    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    db.get_db().commit()
    return {"result": 'You have successfully added a tag to the restaurant!'}

# tags GET method to find the tagId of the given tag
@restaurants.route('/restaurants/findtag/<tagName>', methods=['GET'])
def find_given_tags(tagName):
    sql = '''SELECT tagId FROM Tags WHERE tagName = '{0}' '''.format(tagName)
    current_app.logger.info('GET /restaurants/findtag/<tagName> route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# tags DELETE route to delete a tag 
@restaurants.route('/restaurants/tags/<restId>/<tagId>', methods=['DELETE'])
def delete_tag(restId, tagId):  
    current_app.logger.info('restaurant_routes.py: DELETE /tags/<restId>/<tagId>')

    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM RestaurantTags WHERE restId = {0} AND tagId = {1}".format(restId, tagId))
    db.get_db().commit()

    return 'Tag Removed'

# reviews GET route to return reviews below a given rating
@restaurants.route('/restaurants/reviews/<restId>/<rating>', methods=['GET'])
def get_reviews_below(restId, rating):
    current_app.logger.info('restaurant_routes.py: GET /reviews/<restId>/<itemName>')

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT username, rating, text FROM Restaurants
                        JOIN Reviews  ON Restaurants.restId = Reviews.restId
                        JOIN Users ON Reviews.authorId = Users.userId
                    WHERE rating <= {0} AND Restaurants.restId = {1};'''.format(rating, restId))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# promotions GET route to return all promotions
@restaurants.route('/restaurants/promotions/<restId>', methods=['GET'])
def get_promos(restId):
    current_app.logger.info('restaurant_routes.py: GET /promotions/<restId>')

    cursor = db.get_db().cursor()
    cursor.execute('SELECT name, description, CASE WHEN active = 1 THEN "Yes" ELSE "No" END as activeStatus FROM Promotions WHERE restId = {0};'.format(restId))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# promotions POST route to add a promotion
@restaurants.route('/restaurants/promotions', methods=['POST'])
def add_promo():
    # collecting data from the request object 
    the_data = request.json
    # return the_data
    current_app.logger.info(the_data)
    # extracting the variable
    name = the_data['name']
    desc = the_data['description']
    restId = the_data['restId']
    active = the_data['active']
    # return {"query":"test"}
    # Constructing the query
    sql = '''INSERT into Promotions (name, description, restId, active) values ('{0}', '{1}', {2}, {3})'''.format(name, desc, restId, active)
    current_app.logger.info(sql)
    # return {"query":sql}
    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    db.get_db().commit()
    return {"result": 'You have successfully added a new promotion!'}

# promotions GET route to return info on a specific promotion
@restaurants.route('/restaurants/promotions/<restId>/<name>', methods=['GET'])
def get_promo(restId, name):
    current_app.logger.info('restaurant_routes.py: GET /promotions/<restId>/<name>')

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT name, description, active FROM Promotions WHERE restId = {0} AND LCASE(REPLACE(name, ' ','')) = '{1}';'''.format(restId, str(name).casefold()))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# promotions PUT route to update a promotion
@restaurants.route('/restaurants/promotions/<restId>/<name>', methods=['PUT'])
def update_promotion(restId, name):
    current_app.logger.info('restaurant_routes.py: PUT /promotions/<restId>/<itemName>')
    # collecting data from the request object 
    the_data = request.json
    # return the_data
    current_app.logger.info(the_data)
    # extracting the variable
    new_name = the_data['name']
    desc = the_data['description']
    active = the_data['active']

    cursor = db.get_db().cursor()
    cursor.execute("UPDATE Promotions SET name = '{0}', description = '{1}', active = {2} WHERE restId = {3} AND name = '{4}'".format(new_name, desc, active, restId, name))
    db.get_db().commit()
    return 'Promotion Updated!'

# menuitem DELETE route to delete a menu item
@restaurants.route('/restaurants/promotions/<restId>/<name>', methods=['DELETE'])
def delete_promotion(restId, name):  
    current_app.logger.info('restaurant_routes.py: DELETE /promotions/<restId>/<itemName>')

    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM Promotions WHERE restId = {0} AND LCASE(REPLACE(name, ' ','')) = '{1}'".format(restId, str(name).casefold()))
    db.get_db().commit()

    return 'Promotion Deleted'
    
