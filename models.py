from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=True)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows_venue = db.relationship('Show', backref='venue', lazy="joined", cascade="all, delete")

    def __repr__(self):
        return f'<Venue ID: {self.id}, name:{self.name}, city:{self.city}, state:{self.state}, address:{self.address}, phone:{self.phone}, genres:{self.genres},facebook_link:{self.facebook_link}, image_link:{self.image_link}, website_link:{self.website_link}, seeking_talent:{self.seeking_talent}, seeking_description:{self.seeking_description}>'

    # Done: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=True)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    shows_artist = db.relationship('Show', backref='artist', lazy="joined", cascade="all, delete")

    def __repr__(self):
        return f'<Artist ID: {self.id}, name:{self.name}, city:{self.city}, state:{self.state}, phone:{self.phone}, genres:{self.genres}, facebook_link:{self.facebook_link}, image_link:{self.image_link}, website_link:{self.website_link}, seeking_venue:{self.seeking_venue}, seeking_description:{self.seeking_description}>'

    # DONE: implement any missing fields, as a database migration using Flask-Migrate

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Show_ID:{self.id}, artist_id:{self.artist_id}, venue_id:{self.venue_id}>'

