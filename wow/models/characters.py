from wow import db
from datetime import datetime
class Characters(db.Model):
    __tablename__ = 'characters'
    __bind_key__ = 'characters'
    
    guid = db.Column(db.Integer, primary_key=True, nullable=False)
    account = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(12), unique=True, nullable=False, default='')
    race = db.Column(db.Integer, nullable=False)
    class_ = db.Column('class', db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Integer, nullable=False)
    online = db.Column(db.Integer, nullable=False, default=0)
    totaltime = db.Column(db.Integer, nullable=False, default=0)
    logout_time = db.Column(db.Integer)
    