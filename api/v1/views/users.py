#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    users = storage.all(User).values()
    liusers_list = []
    for user in users:
        liusers_list.append(user.to_dict())
    return jsonify(liusers_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieves an user """
    u = storage.get(User, user_id)
    if not u:
        abort(404)

    return jsonify(u.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user Object
    """

    u = storage.get(User, user_id)

    if not u:
        abort(404)

    storage.delete(u)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    d = request.get_json()
    i = User(**d)
    i.save()
    return make_response(jsonify(i.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """
    Updates a user
    """
    u = storage.get(User, user_id)

    if not u:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    igop = ['id', 'email', 'created_at', 'updated_at']

    dt = request.get_json()
    for key, value in dt.items():
        if key not in igop:
            setattr(u, key, value)
    storage.save()
    return make_response(jsonify(u.to_dict()), 200)
