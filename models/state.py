#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, bs
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, bs):
    """Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        nm = Column(String(128), nullable=False)
        c = relationship("City",
                              backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        nm = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def c(self):
            """getter for list of city instances related to the state"""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
