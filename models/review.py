#!/usr/bin/python
""" holds class Review"""
import models
from models.base_model import BaseModel, bs
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, bs):
    """Representation of Review """
    if models.storage_t == 'db':
        __tablename__ = 'reviews'
        p_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        txt = Column(String(1024), nullable=False)
    else:
        p_id = ""
        user_id = ""
        txt = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
