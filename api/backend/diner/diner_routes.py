########################################################
# Blueprint of endpoints for diners
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

diner = Blueprint('diner', __name__)

# @diner.route('/prediction/<var01>/<var02>', methods=['GET'])
# def predict_value(var01, var02):
#     current_app.logger.info(f'var01 = {var01}')
#     current_app.logger.info(f'var02 = {var02}')

#     returnVal = predict(var01, var02)
#     return_dict = {'result': returnVal}

#     the_response = make_response(jsonify(return_dict))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response


# # Get all diners from the DB
# @restaurants.route('/diner', methods=['GET'])
# def get_restaurants():
#     current_app.logger.info('diner_routes.py: GET /diner')
#     cursor = db.get_db().cursor()
#     cursor.execute('SELECT username FROM users;')
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
# @restaurants.route('/restaurants', methods=['PUT'])
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

# Get reviews from the people that the given userId follows
@diner.route('/diner/<username>', methods=['GET'])
def get_reviews(username):
    current_app.logger.info('GET /diner/<username> route')
    cursor = db.get_db().cursor()
    sql = '''SELECT
            DATE_FORMAT(r.timePosted, '%Y-%m-%d') AS dayPosted,
            u.username,
            r.rating,
            r.text,
            r.photo
        FROM Users me
        JOIN Followers f ON me.userId = f.followerId
        JOIN Reviews r ON f.followeeId = r.authorId
        JOIN Users u ON r.authorId = u.userId
        WHERE me.username = '{0}' '''.format(username)
    cursor.execute(sql)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# add a new review to the app
@diner.route('/diner', methods=['POST'])
def add_new_review():
    
    # collecting data from the request object 
    the_data = request.json
    # return the_data
    current_app.logger.info(the_data)
    # extracting the variable
    rating = the_data['rating']
    # return rating
    text = the_data['text']
    authorId = the_data['authorId']
    restId = the_data['restId']
    photo = the_data['photo']
    # return {"query":"test"}
    # Constructing the query
    sql = '''INSERT into Reviews (rating, text, authorId, restId, photo) values ({0}, '{1}', {2}, {3}, '{4}')'''.format(rating, text, authorId, restId, photo)
    current_app.logger.info(sql)
    # return {"query":sql}
    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    db.get_db().commit()
    return {"result": 'You have successfully added a review!'}


# search for restaurants based on tags
@diner.route('/diner', methods=['GET'])
def search_restaurants():
    # Retrieve the 'tags' query parameter
    tags = request.args.get('tags', default='', type=str)
    sql = '''SELECT DISTINCT
        restName as RestaurantName,
        websiteLink
        FROM Restaurants r
        JOIN RestaurantTags rt ON r.restId = rt.restId
        JOIN Tags t ON rt.tagId = t.tagId
        WHERE rt.tagId in ({0})'''.format(tags)
    # return sql
    current_app.logger.info('GET /diner route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# display all restaurant names
@diner.route('/diner/restaurants', methods=['GET'])
def show_restaurants():
    sql = '''SELECT DISTINCT restId as ID, restName as Name FROM Restaurants r'''
    # return sql
    current_app.logger.info('GET /diner route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# find the user's authorId
@diner.route('/diner/author/<username>', methods=['GET'])
def find_author(username):
    sql = '''SELECT userId FROM Users WHERE username = '{0}' '''.format(username)
    # return sql
    current_app.logger.info('GET /diner route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    theUser = theData[0]
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theUser)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response 

# find list of all tags
@diner.route('/diner/tags', methods=['GET'])
def find_tags():
    sql = '''SELECT tagName, tagId FROM Tags'''
    # return sql
    current_app.logger.info('GET /diner/tags route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response