from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    favorite = db.relationship('Favorite', backref='user', lazy=True)
    def get_id(self):
        return self.user_id

class Spot(db.Model):
    spot_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    favorites = db.relationship('Favorite', backref='spot', lazy=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    wind_speed = db.Column(db.String(50), nullable=True)
    water_direction = db.Column(db.String(50), nullable=True)
    accessibility = db.Column(db.String(100), nullable=True)
    difficulty_level = db.Column(db.Enum('beginner', 'intermediate', 'advanced', name='difficulty_level'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    reviews = db.relationship('Review', backref='spot', lazy=True)

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.spot_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Favorite(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.spot_id'), nullable=False)

class SpotImage(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.spot_id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=True)
