#!/usr/bin/python3
""" Index """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    cs = [Amenity, City, Place, Review, State, User]
    n = ["amenities", "cities", "places", "reviews", "states", "users"]

    n_objs = {}
    for i in range(len(cs)):
        n_objs[n[i]] = storage.count(cs[i])

    return jsonify(n_objs)
