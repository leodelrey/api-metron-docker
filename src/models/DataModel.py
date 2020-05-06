# src/models/DataModel.py
import datetime
from . import db
from marshmallow import fields, Schema
from .Model import Model


class DataModel(Model):
    """
    This is a class to create, read, update and delete Characters

    Attributes:
        id (int): The unique id of the data
        created_date (DateTime): The date of creation
        name (str): The name of the data
        value (float): The age of the data
    """

    __tablename__ = 'data'

    # Data's columns
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    name = db.Column(db.String())
    value = db.Column(db.Float)

    def __init__(self, name, value):
        """
        The constructor for Character class
        Parameters:
           data (dict): The character-related data
        """
        self.created_date = datetime.datetime.utcnow()
        self.name = name
        self.value = value

    @staticmethod
    def get_data():
        """
        The function to get the full list of data in database
        Returns:
           list: The list of data
        """
        return DataModel.query.all()


class DataSchema(Schema):
    """
    This is a Schema class to serialize Data objects
    """
    id = fields.Int(required=True)
    created_date = fields.DateTime()
    name = fields.Str()
    value = fields.Float()
