########################################################
# blueprint of endpoints for data analyst
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

data_analyst = Blueprint('data_analyst', __name__)

@data_analyst.route('/prediction/<var01>/<var02>', methods=['GET'])
    
# [Tom-1] Return each tag and the number of times they were used ordered by popularity
@data_analyst.route('/data_analyst', methods=['GET'])
def get_tags():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT tagName, COUNT(tagName) as NumTimesUsed  \
        FROM RestaurantTags rt JOIN Tags t ON rt.tagId = t.tagId \
        GROUP BY tagName \
        ORDER BY NumTimesUsed desc, tagName asc; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# [Tom-2] Return the number of views and comments of each review
@data_analyst.route('/data_analyst', methods=['GET'])
def get_reviews():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT r.reviewId, COUNT(rv.timeViewed) AS numberOfviews, COUNT(c.commentId) AS numberOfComments \
        FROM Reviews r LEFT JOIN ReviewViews rv on r.reviewId = rv.reviewId LEFT JOIN Comments c on r.reviewId = c.reviewID \
        GROUP BY reviewId; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

    # [Tom-3] Return the customer demographic information for each restaurant
@data_analyst.route('/data_analyst', methods=['GET'])
def get_users():
    current_app.logger.info('data_analyst_routes.py: GET /data_analyst')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT restName as RestaurantName, ROUND(AVG(DATEDIFF(CURRENT_DATE, u.dob) / 365)) as AvgDinerAge, \
        SUM(CASE WHEN r.city != u.city THEN 1 ELSE 0 END) as numNotLocalDiners \
            FROM Restaurants r LEFT JOIN Reviews rv ON r.restID = rv.restId LEFT JOIN Users u ON rv.authorId = u.userId \
            GROUP BY restName; ')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response