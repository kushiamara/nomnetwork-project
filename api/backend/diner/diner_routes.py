########################################################
# Blueprint of endpoints for diners
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

diner = Blueprint('diner', __name__)

@diner.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


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

# Get customer detail for customer with particular userID
@diner.route('/diner/<userId>', methods=['GET'])
def get_reviews(userId):
    current_app.logger.info('GET /diner/<userId> route')
    cursor = db.get_db().cursor()
    cursor.execute(
    '''SELECT
            DATE(r.timePosted) as dayPosted,
            u.username,
            r.rating,
            r.text,
            rp.photo
        FROM Users me
        JOIN Followers f ON me.userId = f.followerId
        JOIN Reviews r ON f.followeeId = r.authorId
        JOIN Users u ON r.authorId = u.userId
        LEFT JOIN ReviewPhotos rp ON r.reviewId = rp.reviewID
        WHERE me.userId = {0}'''.format(userId))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


