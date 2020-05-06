# src/models/HatModel.py
from . import db
import enum
from marshmallow import fields, Schema
from .Model import Model


class ColorType(enum.Enum):
    """
    This is an enum class for the three color types of a hat
    """

    PURPLE = "PURPLE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class HatModel(Model):
    """
    This is a class to create, read, update and delete Hats

    Attributes:
        id (int): The unique id of the hat
        color (Enum(ColorType)): The color of the hat
        character_id (int): The character associated
    """

    __tablename__ = 'hat'

    # Hat's columns
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Enum(ColorType))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    def __init__(self, data):
        """
        The constructor for Hat class.
        Parameters:
           data (dict): The hat-related data
        """
        self.color = data.get('color')
        self.character_id = data.get('character_id')

    @staticmethod
    def get_all_hats():
        """
        The function to get the full list of hats in database
        Returns:
           list: The list of hats
        """
        return HatModel.query.all()

    @staticmethod
    def get_hat(id):
        """
        The function to get a specific hat from database
        Parameters:
            id (int): The primary key of the hat
        Returns:
           HatModel: The hat (None if not found)
        """
        return HatModel.query.get(id)

    @staticmethod
    def get_hat_by_char(id_char):
        """
        The function to get a character-related hat from database
        Parameters:
            id (int): The primary key of the character
        Returns:
           HatModel: The hat (None if not found)
        """
        return HatModel.query.filter_by(character_id=id_char).scalar()

    @staticmethod
    def char_has_hat(id_char):
        """
        The function to check if a character has a hat
        Parameters:
            id (int): The primary key of the character
        Returns:
           bool: True if the character has a hat / False if not
        """
        return HatModel.query.filter_by(character_id=id_char).count() > 0

    @staticmethod
    def verify_hat_rules(char_d, hat_d):
        """
        The function checks if the hat rules are respected
        in the data specified
        Parameters:
            char_d (dict): The parameters of the character
            hat_d (dict): The parameters of the hat
        Returns:
           Response: The response error if rule isn't respected
                    (None if rules are respected)
        """
        # Names with 'p' canno't wear yellow hat
        if (char_d.get('name') and hat_d.get('color') and
                ('p' in char_d.get('name') or 'P' in char_d.get('name')) and
                hat_d.get('color') and hat_d.get('color') == 'YELLOW'):
            return {'error': 'character with \'p\' in his name can\'t wear yellow hat'}
        # Non human characters can't wear hat
        if char_d.get('human') is False:
            return {'error': 'non human character can\'t wear hat'}


# Hat Schema to serialize Hat objects
class HatSchema(Schema):
    """
    This is a Schema class to serialize Hat objects
    """
    id = fields.Int(dump_only=True)
    color = fields.Str(required=True)
