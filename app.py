#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask.json import jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref
from sqlalchemy.sql.elements import True_
from forms import *
from datetime import datetime

import sys

from models import db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)

# DONE: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

    # Done: implement any missing fields, as a database migration using Flask-Migrate

    # DONE: implement any missing fields, as a database migration using Flask-Migrate

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues-----------------------------------------------------------------------------
#  -----------------------------------------------------------------------------------
@app.route('/venues')
def venues():
    # DONE: replace with real venues data.
    # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    
    data = []    
    areas = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state).order_by('state').all()
    for area in areas:
        venues = Venue.query.filter_by(state=area.state).filter_by(city=area.city).order_by('name').all()
        venue_data = []
        data.append({
            'city':area.city,
            'state':area.state,
            'venues': venue_data,
        })
        for venue in venues:
            shows = Show.query.filter_by(venue_id=venue.id).order_by('id').all()
            venue_data.append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len(shows)
            })

    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term', None)
    
    venues = Venue.query.filter(Venue.name.ilike("%{}%".format(search_term))).all()
    
    data = []

    for venue in venues:
        num_upcoming_shows = 0

        shows = Show.query.filter('venue_id' == venue.id).all()
        for show in shows:
            if(show.start_time > datetime.now()):
                num_upcoming_shows += 1            
        
        data.append({
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': num_upcoming_shows
        })

    response = {
        "count": len(venues),
        "data": data
    }
    
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
# shows the venue page with the given venue_id
# DID it: replace with real venue data from the venues table, using venue_id
def show_venue(venue_id):

    past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.venue_id == venue_id, Show.artist_id == Artist.id, Show.start_time < datetime.now()).all()
    
    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.venue_id == venue_id, Show.artist_id == Artist.id, Show.start_time > datetime.now()).all()

    venue = Venue.query.get_or_404(venue_id)

    venue_data = {
        'id':venue_id,
        'name':venue.name,
        'genres':venue.genres,
        'city':venue.city,
        'state':venue.state,
        'address': venue.address,
        'phone': venue.phone,
        'website':venue.website_link,
        'facebook_link':venue.facebook_link,
        'image_link':venue.image_link,
        'seeking_talent':venue.seeking_talent,
        'seeking_description':venue.seeking_description,
        'past_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in past_shows],
        'upcoming_shows': [{
            'artist_id':artist.id,
            'artist_name':artist.name,
            'artist_image_link':artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }
  
    return render_template('pages/show_venue.html', venue=venue_data)

# --------------------------------------------------------------------------------
#  Create Venue ------------------------------------------------------------------
#  -------------------------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    error = False
    try:
        newVenue = Venue(
            name=form.name.data, 
            city=form.city.data, 
            state=form.state.data, 
            address= form.address.data, 
            phone=form.phone.data, 
            genres= form.genres.data, 
            facebook_link=form.facebook_link.data, 
            image_link=form.image_link.data, 
            website_link=form.website_link.data, 
            seeking_description=form.seeking_description.data, 
            seeking_talent=form.seeking_talent.data)        
        
        db.session.add(newVenue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    
    return render_template('pages/home.html')
    

@app.route('/venues/<int:venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)

        shows = Show.query.filter_by(venue_id=venue.id).order_by('id').all()
        
        for show in shows:
            db.session.delete(show)

        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    
    return(render_template(url_for('index')))

  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    
# ------------------------------------------------------------------------------------
#  Artists ---------------------------------------------------------------------------
#  -----------------------------------------------------------------------------------
@app.route('/artists')
def artists():
    artist_data = Artist.query.all()

  # DONE: replace with real data returned from querying the database
    return render_template('pages/artists.html', artists=artist_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term', '')

    artists = Artist.query.filter(Artist.name.ilike("%{}%".format(search_term))).all()
    
    data = []

    for artist in artists:
        num_upcoming_shows = 0

        shows = Show.query.filter('artist_id' == artist.id).all()
        for show in shows:
            if(show.start_time > datetime.now()):
                num_upcoming_shows += 1
        
        data.append({
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': num_upcoming_shows
        })

        response = {
            'count':len(artists),
            'data':data
        }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get(artist_id)
    
    past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.venue_id == Venue.id, Show.artist_id == Artist.id, Show.start_time < datetime.now()).all()
    
    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.venue_id == Venue.id, Show.artist_id == Artist.id, Show.start_time > datetime.now()).all()

    venue = Venue.query.filter_by(id=Venue.id).first_or_404()

    artist_data = {
        'id':artist.id,
        'name':artist.name,
        'city':artist.city,
        'state':artist.state,
        'genres':artist.genres,
        'phone':artist.phone,
        'website_link':artist.website_link,
        'facebook_link':artist.facebook_link,
        'image_link':artist.image_link,
        'seeking_venue':artist.seeking_venue,
        'seeking_description':artist.seeking_description,
        'past_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in past_shows],
        'upcoming_shows': [{
            'artist_id':artist.id,
            'artist_name':artist.name,
            'venue_image_link':venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }
    
    return render_template('pages/show_artist.html', artist=artist_data)

# ------------------------------------------------------------------------------------
#  Update ----------------------------------------------------------------------------
#  -----------------------------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    
    form = ArtistForm()    
    
    # DONE: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    error = False
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get(artist_id)
        # Updating records
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.website_link = form.website_link.data
        artist.seeking_description = form.seeking_description .data
        artist.seeking_venue = form.seeking_venue.data
        #Saving transaction
        db.session.commit()
        error = True
    except:
        # rolling back transaction
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    venue = Venue.query.get(venue_id)

    # DONE: populate form with values from venue with ID <venue_id>    
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()
    # DONE: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    error = False
    try:
        venue = Venue.query.get(venue_id)
        # Updating records
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.genres = form.genres.data
        venue.website_link = form.website_link.data
        venue.seeking_description = form.seeking_description.data
        venue.seeking_talent = form.seeking_talent.data
       #Saving transaction
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' +venue.name+ ' could not be updated.')
    
    return redirect(url_for('show_venue', venue_id=venue_id))
# ------------------------------------------------------------------------------------
#  Create Artist ---------------------------------------------------------------------
# ------------------------------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    error = False
    try:
        newArtist = Artist(
            name=form.name.data, 
            city=form.city.data, 
            state=form.state.data, 
            phone=form.phone.data, 
            genres= form.genres.data, 
            facebook_link=form.facebook_link.data, 
            image_link=form.image_link.data, 
            website_link=form.website_link.data, 
            seeking_description=form.seeking_description.data, 
            seeking_venue=form.seeking_venue.data)
        
        db.session.add(newArtist)
        db.session.commit()
        
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        abort(500)
    
    return render_template('pages/home.html')

# ------------------------------------------------------------------------------------
#  Shows -----------------------------------------------------------------------------
#  -----------------------------------------------------------------------------------

@ app.route('/shows')
def shows():
    shows = Show.query.order_by(Show.start_time.desc()).all()
    data = []
    for show in shows:
        venue = Venue.query.filter_by(id=show.venue_id).first_or_404()
        artist = Artist.query.filter_by(id=show.artist_id).first_or_404()

        data.append({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        })

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    error = False
    # called to create new shows in the db, upon submitting new show listing form
    # DONE: insert form data as a new Show record in the db, instead
    try:
        newShow = Show(artist_id=form.artist_id.data, venue_id=form.venue_id.data, start_time=form.start_time.data)
        db.session.add(newShow)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
        abort(500)
    return render_template('pages/home.html')
    # DONE: on successful db insert, flash success
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
