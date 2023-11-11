#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities(state_id):
    """
    Retrieves the list of all cities objects
    of a specific State, or a specific city
    """
    l_cities = []
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    for city in st.cities:
        l_cities.append(city.to_dict())

    return jsonify(l_cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """
    Retrieves a specific city based on id
    """
    c = storage.get(City, city_id)
    if not c:
        abort(404)
    return jsonify(c.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a city based on id provided
    """
    c = storage.get(City, city_id)

    if not c:
        abort(404)
    storage.delete(c)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def post_city(state_id):
    """
    Creates a City
    """
    s = storage.get(State, state_id)
    if not s:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    d = request.get_json()
    i = City(**d)
    i.state_id = s.id
    i.save()
    return make_response(jsonify(i.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """
    Updates a City
    """
    c = storage.get(City, city_id)
    if not c:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    igo = ['id', 'state_id', 'created_at', 'updated_at']

    d = request.get_json()
    for key, value in d.items():
        if key not in igo:
            setattr(c, key, value)
    storage.save()
    return make_response(jsonify(c.to_dict()), 200)
