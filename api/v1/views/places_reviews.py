#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Reviews """
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    p = storage.get(Place, place_id)

    if not p:
        abort(404)

    rw = [review.to_dict() for review in p.reviews]

    return jsonify(rw)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object
    """
    rw = storage.get(Review, review_id)
    if not rw:
        abort(404)

    return jsonify(rw.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete_reviews.yml', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review Object
    """

    rw = storage.get(Review, review_id)

    if not rw:
        abort(404)

    storage.delete(rw)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def post_review(place_id):
    """
    Creates a Review
    """
    pc = storage.get(Place, place_id)

    if not pc:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    dt = request.get_json()
    ur = storage.get(User, dt['user_id'])

    if not ur:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    dt['place_id'] = place_id
    sc = Review(**dt)
    sc.save()
    return make_response(jsonify(sc.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def put_review(review_id):
    """
    Updates a Review
    """
    rw = storage.get(Review, review_id)

    if not rw:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    igo = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    dt = request.get_json()
    for key, value in dt.items():
        if key not in igo:
            setattr(rw, key, value)
    storage.save()
    return make_response(jsonify(rw.to_dict()), 200)
