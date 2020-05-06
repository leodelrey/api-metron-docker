# src/models/CharacterModel.py
from . import db
from marshmallow import fields, Schema
from sqlalchemy.orm import relationship
from .HatModel import HatSchema
from .Model import Model


class CharacterModel(Model):
    """
    This is a class to create, read, update and delete Characters

    Attributes:
        id (int): The unique id of the character
        name (str): The name of the character
        age (int): The age of the character
        weight (float): The weight of the character
        human (boolean): The character is human or not
    """

    __tablename__ = 'character'

    # Character's columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    human = db.Column(db.Boolean)
    hat = relationship("HatModel", uselist=False, backref="character")

    def __init__(self, data):
        """
        The constructor for Character class.
        Parameters:
           data (dict): The character-related data
        """
        self.name = data.get('name')
        self.age = data.get('age')
        self.weight = data.get('weight')
        self.human = data.get('human')
        self.hat = data.get('hat')

    @staticmethod
    def get_all_chars():
        """
        The function to get the full list of characters in database
        Returns:
           list: The list of characters
        """
        return CharacterModel.query.all()

    @staticmethod
    def get_char(id):
        """
        The function to get a specific character from database
        Parameters:
            id (int): The primary key of the character
        Returns:
           CharacterModel: The character (None if not found)
        """
        return CharacterModel.query.get(id)

    @staticmethod
    def verify_char_rules(data):
        """
        The function checks if the character rules are respected
        in the data specified
        Parameters:
            data (dict): The parameters of the character
        Returns:
           Response: The response error if rule isn't respected
                    (None if rules are respected)
        """
        # Age must be a positive number
        if data.get('age') and data.get('age') <= 0:
            return {'error': 'age is not a positive number'}

        # Human characters with weight > 80 canno't be under 10 years old
        if (data.get('human') and data.get('weight') and data.get('age') and
                data.get('weight') > 80 and data.get('age') <= 10):
            return {'error': 'character is too fat (>80) to be under 10 years old'}

    def __repr(self):
        return '<id {}>'.format(self.id)


class CharacterSchema(Schema):
    """
    This is a Schema class to serialize Character objects
    """
    id = fields.Int(required=True)
    name = fields.Str()
    age = fields.Int()
    weight = fields.Float()
    human = fields.Bool()
    hat = fields.Nested(HatSchema)
