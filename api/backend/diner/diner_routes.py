########################################################
# Blueprint of endpoints for diners
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

diner = Blueprint('diner', __name__)

# [Emily-3]
# Get reviews for the people that the given userId follows
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
        WHERE me.username = '{0}' 
        ORDER BY dayPosted desc'''.format(username)
    cursor.execute(sql)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# [Emily-2]
# add a new review to the app
@diner.route('/diner', methods=['POST'])
def add_new_review():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)
    # extracting the variable
    rating = the_data['rating']
    text = the_data['text']
    authorId = the_data['authorId']
    restId = the_data['restId']
    photo = the_data['photo']
    # Constructing the query
    sql = '''INSERT into Reviews (rating, text, authorId, restId, photo) values ({0}, '{1}', {2}, {3}, '{4}')'''.format(rating, text, authorId, restId, photo)
    current_app.logger.info(sql)
    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    db.get_db().commit()
    return {"result": 'You have successfully added a review!'}


# display all restaurant names to be displayed in post review dropdown
@diner.route('/diner/restaurants', methods=['GET'])
def show_restaurants():
    sql = '''SELECT DISTINCT restId as ID, restName as Name FROM Restaurants r'''
    current_app.logger.info('GET /diner route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# find the user's authorId to insert when posting a review
@diner.route('/diner/author/<username>', methods=['GET'])
def find_author(username):
    sql = '''SELECT userId FROM Users WHERE username = '{0}' '''.format(username)
    current_app.logger.info('GET /diner route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    theData = cursor.fetchall()
    theUser = theData[0]
    the_response = make_response(theUser)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response 


# [Emily-1]
# find list of all tags to display in the dropdown
@diner.route('/diner/tags', methods=['GET'])
def find_tags():
    sql = '''SELECT tagName, tagId FROM Tags'''
    current_app.logger.info('GET /diner/tags route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# search for restaurants based on tags
@diner.route('/diner/restaurants/search', methods=['GET'])
def search_restaurants():
    # Retrieve the 'tags' query parameter
    tags = request.args.get('tags', default='', type=str)
    tags_length = len(tags.split(","))
    sql = '''SELECT DISTINCT
        restName as RestaurantName,
        websiteLink
        FROM Restaurants r
        JOIN RestaurantTags rt ON r.restId = rt.restId
        JOIN Tags t ON rt.tagId = t.tagId
        WHERE rt.tagId in ({0})
        GROUP BY r.restName, r.websiteLink
        HAVING COUNT(DISTINCT t.tagName) = {1} '''.format(tags, tags_length)
    current_app.logger.info('GET /diner route')
    cursor = db.get_db().cursor()
    cursor.execute(sql)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response