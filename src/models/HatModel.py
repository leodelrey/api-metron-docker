# src/models/hat.py
from . import db
import enum
class ColorType(enum.Enum):
    PURPLE = "Purple"
    YELLOW = "Yellow"
    GREEN = "Green"

class HatModel(db.model):
    """
    Hat Model
    """
    __tablename__ = 'hat'

    id = db.Column(db.Integer,primay_key=True)
    color = db.Column(db.Enum(ColorType))

    # class constructor
    def __init__(self, color):
        """
        Class constructor
        """
        self.name = name
        self.color = color

    def serialize(self):
        return {
            'id': self.id, 
            'color': self.color,

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
        setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)


    def __repr(self):
        return '<id {}>'.format(self.id)