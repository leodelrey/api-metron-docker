# src/models/CharacterModel.py
from . import db


class Model(db.Model):
    """
    This is a class to define save, update and delete methods.
    """
    __abstract__ = True

    def save(self):
        """
        The method to save an object in database
        """
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """
        The method to update an object in database

        Parameters:
            data (dict): The data to update
        """
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        """
        The method to delete an object from database
        """
        db.session.delete(self)
        db.session.commit()
