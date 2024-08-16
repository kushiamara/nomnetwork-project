########################################################
# blueprint of endpoints for data analyst
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

data_analyst = Blueprint('data_analyst', __name__)

# [Tom-1] Return each resturuant ranked by rating and number of reviews 
@data_analyst.route('/data_analyst/rest', methods=['GET'])
def get_rest():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst/rest')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT restName as RestaurantName, AVG(rating) as AverageRating, COUNT(reviewId) as NumberOfReviews \
        FROM Restaurants r JOIN Reviews re ON r.restId=re.restId  \
        GROUP BY restName \
        ORDER BY AverageRating desc, NumberOfReviews desc \
        LIMIT 20 ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response 

# [Tom-1] Return each tag and the number of times they were used ordered by popularity
@data_analyst.route('/data_analyst/tags', methods=['GET'])
def get_tags():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst/tags')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT tagName, COUNT(tagName) as NumTimesUsed  \
        FROM RestaurantTags rt JOIN Tags t ON rt.tagId = t.tagId \
        GROUP BY tagName \
        ORDER BY NumTimesUsed desc, tagName asc \
        LIMIT 20; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# [Tom-2.1.1] Return the number of views and comments of each review
# DIDNT USE
@data_analyst.route('/data_analyst/behavior', methods=['GET'])
def get_reviews():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst/behavior')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT r.reviewId, COUNT(rv.timeViewed) AS numberOfviews, COUNT(c.commentId) AS numberOfComments \
        FROM Reviews r LEFT JOIN ReviewViews rv on r.reviewId = rv.reviewId LEFT JOIN Comments c on r.reviewId = c.reviewID \
        GROUP BY reviewId; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# [Tom-2.1.2] Return the reviews with the highest views and comments 
@data_analyst.route('/data_analyst/behavior/high', methods=['GET'])
def get_reviews_high():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst/behavior/high')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.username, r.reviewId, COUNT(rv.timeViewed) AS NumberOfViews, COUNT(c.commentId) AS NumberOfComments \
        FROM Reviews r LEFT JOIN ReviewViews rv on r.reviewId = rv.reviewId LEFT JOIN Comments c on r.reviewId = c.reviewID JOIN Users u on u.userId=r.authorId\
        GROUP BY reviewId \
        ORDER BY NumberOfViews desc, NumberOfComments desc \
        LIMIT 15; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# [Tom-2.1.3] Return the reviews with the highest views and lowest comments 
@data_analyst.route('/data_analyst/behavior/low', methods=['GET'])
def get_reviews_low():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst/behavior/low')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.username, r.reviewId, COUNT(rv.timeViewed) AS NumberOfViews, COUNT(c.commentId) AS NumberOfComments \
        FROM Reviews r LEFT JOIN ReviewViews rv on r.reviewId = rv.reviewId LEFT JOIN Comments c on r.reviewId = c.reviewID JOIN Users u on u.userId=r.authorId\
        GROUP BY reviewId \
        ORDER BY NumberOfViews desc, NumberOfComments asc \
        LIMIT 15; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# [Tom-2.2.1] Return the users with the most followers and the amount of reviews they have posted
@data_analyst.route('/data_analyst/behavior/followers', methods=['GET'])
def get_followers():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst/behavior/followers')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.username, COUNT(r.reviewId) as NumberOfReviews, COUNT(f.followerId) as NumberOfFollowers \
        FROM Reviews r JOIN Users u on u.userId=r.authorId JOIN Followers f ON f.followeeId=u.userId\
        GROUP BY u.username \
        ORDER BY NumberOfFollowers desc\
        LIMIT 20; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

    # [Tom-3] Return the customer demographic information for each restaurant
@data_analyst.route('/data_analyst/users', methods=['GET'])
def get_users():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst/users')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT restName as RestaurantName, ROUND(AVG(DATEDIFF(CURRENT_DATE, u.dob) / 365)) as AvgDinerAge, \
        SUM(CASE WHEN r.city != u.city THEN 1 ELSE 0 END) as NumberOfNotLocalDiners \
            FROM Restaurants r LEFT JOIN Reviews rv ON r.restID = rv.restId LEFT JOIN Users u ON rv.authorId = u.userId \
            GROUP BY restName; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response