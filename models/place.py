#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, bs
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == 'db':
    place_amenity = Table('place_amenity', bs.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Place(BaseModel, bs):
    """Representation of Place """
    if models.storage_t == 'db':
        __tablename__ = 'places'
        c_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        u_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        n = Column(String(128), nullable=False)
        des = Column(String(1024), nullable=True)
        nu_rooms = Column(Integer, nullable=False, default=0)
        nu_bathrooms = Column(Integer, nullable=False, default=0)
        mx_guest = Column(Integer, nullable=False, default=0)
        price_night = Column(Integer, nullable=False, default=0)
        lat = Column(Float, nullable=True)
        t_longitude = Column(Float, nullable=True)
        reviews = relationship("Review",
                               backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity",
                                 secondary=place_amenity,
                                 viewonly=False)
    else:
        c_id = ""
        u_id = ""
        n = ""
        des = ""
        nu_rooms = 0
        nu_bathrooms = 0
        mx_guest = 0
        price_night = 0
        lat = 0.0
        t_longitude = 0.0
        am_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            rw_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    rw_list.append(review)
            return rw_list

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list
