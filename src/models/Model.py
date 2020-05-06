# src/models/CharacterModel.py
from . import db
class Model(db.Model):
    """ 
    This is a class to define generic save, update and delete functions.
    """
    __abstract__ = True

    def save(self):
        """ 
        The function to save an object in database 
        """
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """ 
        The function to update an object in database

        Parameters: 
            data (dict): The data to update
        """
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        """ 
        The function to delete an object from database
        """
        db.session.delete(self)
        db.session.commit()
    