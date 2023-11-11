#!/usr/bin/python
""" holds class Amenity"""
import models
from models.base_model import BaseModel, bs
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, bs):
    """Representation of Amenity """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        n = Column(String(128), nullable=False)
    else:
        n = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
