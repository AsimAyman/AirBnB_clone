#!/usr/bin/python3
"""
Contains the TestPlaceDocs classes
"""

from datetime import datetime
import inspect
import models
from models import place
from models.base_model import BaseModel
import pep8
import unittest
Place = place.Place


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Place class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.place_f = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place(self):
        """Test that models/place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_place(self):
        """Test that tests/test_models/test_place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_place_module_docstring(self):
        """Test for the place.py module docstring"""
        self.assertIsNot(place.__doc__, None,
                         "place.py needs a docstring")
        self.assertTrue(len(place.__doc__) >= 1,
                        "place.py needs a docstring")

    def test_place_class_docstring(self):
        """Test for the Place class docstring"""
        self.assertIsNot(Place.__doc__, None,
                         "Place class needs a docstring")
        self.assertTrue(len(Place.__doc__) >= 1,
                        "Place class needs a docstring")

    def test_place_func_docstrings(self):
        """Test for the presence of docstrings in Place methods"""
        for func in self.place_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestPlace(unittest.TestCase):
    """Test the Place class"""
    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))

    def test_city_id_attr(self):
        """Test Place has attr city_id, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))
        if models.storage_t == 'db':
            self.assertEqual(place.c_id, None)
        else:
            self.assertEqual(place.c_id, "")

    def test_user_id_attr(self):
        """Test Place has attr user_id, and it's an empty string"""
        p = Place()
        self.assertTrue(hasattr(p, "user_id"))
        if models.storage_t == 'db':
            self.assertEqual(p.u_id, None)
        else:
            self.assertEqual(p.u_id, "")

    def test_name_attr(self):
        """Test Place has attr name, and it's an empty string"""
        p = Place()
        self.assertTrue(hasattr(p, "name"))
        if models.storage_t == 'db':
            self.assertEqual(p.n, None)
        else:
            self.assertEqual(p.n, "")

    def test_description_attr(self):
        """Test Place has attr description, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "description"))
        if models.storage_t == 'db':
            self.assertEqual(place.des, None)
        else:
            self.assertEqual(place.des, "")

    def test_number_rooms_attr(self):
        """Test Place has attr number_rooms, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_rooms"))
        if models.storage_t == 'db':
            self.assertEqual(place.nu_rooms, None)
        else:
            self.assertEqual(type(place.nu_rooms), int)
            self.assertEqual(place.nu_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Test Place has attr number_bathrooms, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_bathrooms"))
        if models.storage_t == 'db':
            self.assertEqual(place.nu_bathrooms, None)
        else:
            self.assertEqual(type(place.nu_bathrooms), int)
            self.assertEqual(place.nu_bathrooms, 0)

    def test_max_guest_attr(self):
        """Test Place has attr max_guest, and it's an int == 0"""
        p = Place()
        self.assertTrue(hasattr(p, "max_guest"))
        if models.storage_t == 'db':
            self.assertEqual(p.mx_guest, None)
        else:
            self.assertEqual(type(p.mx_guest), int)
            self.assertEqual(p.mx_guest, 0)

    def test_price_by_night_attr(self):
        """Test Place has attr price_by_night, and it's an int == 0"""
        p = Place()
        self.assertTrue(hasattr(p, "price_by_night"))
        if models.storage_t == 'db':
            self.assertEqual(p.price_night, None)
        else:
            self.assertEqual(type(p.price_night), int)
            self.assertEqual(p.price_night, 0)

    def test_latitude_attr(self):
        """Test Place has attr latitude, and it's a float == 0.0"""
        p = Place()
        self.assertTrue(hasattr(p, "latitude"))
        if models.storage_t == 'db':
            self.assertEqual(p.lat, None)
        else:
            self.assertEqual(type(p.lat), float)
            self.assertEqual(p.lat, 0.0)

    def test_longitude_attr(self):
        """Test Place has attr longitude, and it's a float == 0.0"""
        p = Place()
        self.assertTrue(hasattr(p, "longitude"))
        if models.storage_t == 'db':
            self.assertEqual(p.t_longitude, None)
        else:
            self.assertEqual(type(p.t_longitude), float)
            self.assertEqual(p.t_longitude, 0.0)

    @unittest.skipIf(models.storage_t == 'db', "not testing File Storage")
    def test_amenity_ids_attr(self):
        """Test Place has attr amenity_ids, and it's an empty list"""
        p = Place()
        self.assertTrue(hasattr(p, "amenity_ids"))
        self.assertEqual(type(p.am_ids), list)
        self.assertEqual(len(p.am_ids), 0)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        p = Place()
        new_d = p.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in p.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        p = Place()
        new_d = p.to_dict()
        self.assertEqual(new_d["__class__"], "Place")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], p.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], p.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        place = Place()
        string = "[Place] ({}) {}".format(place.id, place.__dict__)
        self.assertEqual(string, str(place))