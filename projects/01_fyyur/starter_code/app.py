#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    venue_name = db.Column(db.String)
    venue_image_link = db.Column(db.String(500))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    artist_name = db.Column(db.String)
    artist_image_link = db.Column(db.String(500))
    start_time = db.Column(db.String(50))

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    venues = Venue.query.all()
    citystates = []

    for venue in venues:
        citystates.append((venue.city, venue.state))

    areas_set = set(citystates)

    for area in areas_set:
        venue_list = []
        for venue in Venue.query.filter_by(state=area[1]).filter_by(city=area[0]).all():
            venue_list.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": db.session.query(Show).filter_by(venue_id = venue.id).filter(Show.start_time > str(datetime.now())).count()
            })
        data.append({
            "city": area[0],
            "state": area[1],
            "venues": venue_list
        })
    return render_template('pages/venues.html', areas=data);
# Done

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    name = request.form.get('search_term', '')
    search = "%{}%".format(name) # % is substring on both sides.
    results = Venue.query.filter(Venue.name.ilike(search)).all()
    data = []

    for result in results:
        venue = {
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": db.session.query(Show).filter_by(venue_id = result.id).filter(Show.start_time > str(datetime.now())).count()
        }
        data.append(venue)

    response={
        "count": len(results),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# Done

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    shows = venue.shows
    now = str(datetime.now())

    past_shows = []
    past_shows_count = 0
    upcoming_shows = []
    upcoming_shows_count = 0
    if shows:
        for show in shows:
            showdata = {
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": show.start_time
            }
            if show.start_time < now:
                past_shows.append(showdata)
                past_shows_count += 1
            else:
                upcoming_shows.append(showdata)
                upcoming_shows_count += 1

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count
    }
    return render_template('pages/show_venue.html', venue=data)
# Done

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False

    try:
        fetchdata = {
            "name": request.form['name'],
            "genres": request.form.getlist('genres'),
            "address": request.form['address'],
            "city": request.form['city'],
            "state": request.form['state'],
            "phone": request.form['phone'],
            #"website": venue.website,
            "facebook_link": request.form['facebook_link'],
            #"seeking_talent": venue.seeking_talent,
            #"seeking_description": venue.seeking_description,
            "image_link": request.form['image_link']
        }
        venue = Venue(**fetchdata)
        db.session.add(venue)
        db.session.commit()

    except:
        # error flag
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    if error:
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    else:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
# Done

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        venue = Venue.query.get(todo_id)
        db.session.delete(venue)
        db.session.commit()

    except:
        error = True # error flag
        db.session.rollback()
        print(sys.exc_info())
    
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Venue ID ' + venue_id + ' could not be listed.')
    else:
        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage
        flash('Venue ID ' + venue_id + ' has been deleted from database.')
        return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    # Done
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    name = request.form.get('search_term', '')
    search = "%{}%".format(name) # % is substring on both sides.
    results = Artist.query.filter(Artist.name.ilike(search)).all()
    data = []

    for result in results:
        artist = {
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": db.session.query(Show).filter_by(venue_id = result.id).filter(Show.start_time > str(datetime.now())).count()
        }
        data.append(artist)

    response={
        "count": len(results),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

# Done

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    artist = Artist.query.get(artist_id)

    shows = artist.shows
    now = str(datetime.now())

    past_shows = []
    past_shows_count = 0
    upcoming_shows = []
    upcoming_shows_count = 0
    if shows:
        for show in shows:
            showdata = {
            "venue_id": show.venue_id,
            "venue_name": show.venue_name,
            "venue_image_link": show.venue_image_link,
            "start_time": show.start_time
            }
            if show.start_time < now:
                past_shows.append(showdata)
                past_shows_count += 1
            else:
                upcoming_shows.append(showdata)
                upcoming_shows_count += 1

    data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count
    }
    
    return render_template('pages/show_artist.html', artist=data)
# Done

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # TODO: populate form with fields from artist with ID <artist_id>
    instance = Artist.query.get(artist_id)
    artist={
        "id": artist_id,
        "name": instance.name,
        "genres": instance.genres,
        "city": instance.city,
        "state": instance.state,
        "phone": instance.phone,
        "website": instance.website,
        "facebook_link": instance.facebook_link,
        "seeking_venue": instance.seeking_venue,
        "seeking_description": instance.seeking_description,
        "image_link": instance.image_link
    }
    return render_template('forms/edit_artist.html', form=form, artist=artist)
    # Done

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    error = False
    
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form['name']
        artist.genres = request.form.getlist('genres')
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.facebook_link = request.form['facebook_link']
        artist.image_link = request.form['image_link']

        db.session.commit()

    except:
        # error flag
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    if error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')

    else:
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
        return redirect(url_for('show_artist', artist_id=artist_id))
    # Done

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    instance = Venue.query.get(venue_id)

    venue={
        "id": instance.id,
        "name": instance.name,
        "genres": instance.genres,
        "address": instance.address,
        "city": instance.city,
        "state": instance.state,
        "phone": instance.phone,
        "website": instance.website,
        "facebook_link": instance.facebook_link,
        "seeking_talent": instance.seeking_talent,
        "seeking_description": instance.seeking_description,
        "image_link": instance.image_link
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)
    # Done

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    error = False
    
    try:
        venue = Artist.query.get(venue_id)
        venue.name = request.form['name']
        venue.genres = request.form.getlist('genres')
        venue.address = request.form['address']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.phone = request.form['phone']
        venue.facebook_link = request.form['facebook_link']
        venue.image_link = request.form['image_link']

        db.session.commit()

    except:
        # error flag
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    if error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')

    else:
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
        return redirect(url_for('show_venue', venue_id=venue_id))
    # Done

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    error = False
    
    try:
        fetchdata = {
            "name": request.form['name'],
            "genres": request.form.getlist('genres'),
            "city": request.form['city'],
            "state": request.form['state'],
            "phone": request.form['phone'],
            #"website": venue.website,
            "facebook_link": request.form['facebook_link'],
            #"seeking_talent": venue.seeking_talent,
            #"seeking_description": venue.seeking_description,
            "image_link": request.form['image_link']
        }
        artist = Artist(**fetchdata)
        db.session.add(artist)
        db.session.commit()

    except:
        # error flag
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    if error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

    else:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
    #Done

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data=Show.query.all()
    # Done
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    error = False
    artist_id = request.form['artist_id']
    artist = Artist.query.get(artist_id)
    venue_id = request.form['venue_id']
    venue = Venue.query.get(venue_id)
    try:
        fetchdata = {
            "artist_id": artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "venue_id": venue_id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": request.form['start_time'],

        }
        show = Show(**fetchdata)
        db.session.add(show)
        db.session.commit()

    except:
        # error flag
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    if error:
        flash('An error occurred. The show could not be listed.')

    else:
        # on successful db insert, flash success
        flash('Show was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')
    # Done

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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
