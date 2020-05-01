# src/models/character.py
from . import db

class CharacterModel(db.Model):
    """
    Character Model
    """

    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    human = db.Column(db.Boolean)
    hat = db.column(db.Integer,Foreign_key('hat.id'))

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.age = data.get('age')
        self.weight = data.get('weight')
        self.human = data.get('human')
        self.hat = data.get('hat')

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'age': self.age,
            'weight':self.weight,
            'human':self.human
        }

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