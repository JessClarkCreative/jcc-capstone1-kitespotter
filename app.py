from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
from flask_login import LoginManager, login_user, logout_user, login_required, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Spot, Review, Favorite, SpotImage, connect_db

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/api/maps-url/<float:latitude>/<float:longitude>')
def maps_url(latitude, longitude):
    GOOGLE_MAPS_API_KEY = Config.GOOGLE_MAPS_API_KEY
    maps_url = f'https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_API_KEY}&q={latitude},{longitude}'
    return jsonify({'url': maps_url})

def get_weather_data(latitude, longitude):
    api_key = Config.WEATHER_API_KEY
    url = f'http://api.weatherstack.com/current?access_key={api_key}&query={latitude},{longitude}'
    response = requests.get(url)
    data = response.json()
    
    # Extract relevant weather data from the response
    if 'current' in data:
        current_weather = data['current']
        weather_info = {
            'temperature': current_weather.get('temperature'),
            'weather_descriptions': current_weather.get('weather_descriptions', []),
            'wind_speed': current_weather.get('wind_speed'),
        }
    else:
        weather_info = {'error': 'Weather data not available'}

    return weather_info

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get((user_id))

@app.route('/')
def home():
    spots = Spot.query.all()
    return render_template('home.html', GOOGLE_MAPS_API_KEY=Config.GOOGLE_MAPS_API_KEY, spots=spots)

@app.route('/spot/<int:spot_id>')
def spot_details(spot_id):
    spot = Spot.query.get_or_404(spot_id)
    weather = get_weather_data(spot.latitude, spot.longitude)
    return render_template('spot_details.html', spot=spot, weather=weather)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('profile.html')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # checking if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return render_template('register.html', error="Username or email already exists.")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback() # roll back any changes made
            return render_template('register.html', error=f"An error occured: {e}")
    return render_template('register.html')

@app.route('/api/save-marker', methods=['POST'])
def save_marker():
    data = request.get_json()
    print("Received data:", data)
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    name = data.get('name')

    if not name or latitude is None or longitude is None:
        return jsonify({'error': 'Missing required fields'}), 400

    # Here you would save the latitude and longitude to your database
    new_spot = Spot(name=name, latitude=latitude, longitude=longitude)
    
    try:
        db.session.add(new_spot)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("error saving marker:", e)
        return jsonify({'error': 'Failed to save marker'}), 500

    return jsonify({'message': 'Marker saved successfully!', 'spot_id': new_spot.spot_id, 'latitude': latitude, 'longitude': longitude}), 201

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)

