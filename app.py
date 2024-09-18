from flask import Flask, render_template, redirect, url_for, request
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
    return User.query.get(int(user_id))

@app.route('/')
def home():
    spots = Spot.query.all()
    
    return render_template('home.html', spots=spots)

@app.route('/spot/<int:spot_id>')
def spot_details(spot_id):
    spot = Spot.query.get_or_404(spot_id)
    weather = get_weather_data(spot.latitude, spot.longitude)
    return render_template('spot_details.html', spot=spot, weather=weather)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html')
    
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
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)

