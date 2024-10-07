import unittest
from app import app, db, User, Spot
from flask_login import login_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
import os

#In terminal use python -m unittest tests.py to run tests

class KiteSpotAppTests(unittest.TestCase):

#Set up test environment
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        
        # Use a test database URI for the tests
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'postgresql://user:password@localhost/test_db')
        
        cls.client = cls.app.test_client()
        
        # Create a new database session
        cls.engine = create_engine(cls.app.config['SQLALCHEMY_DATABASE_URI'])
        cls.connection = cls.engine.connect()
        cls.session = sessionmaker(bind=cls.engine)() 
        
        with cls.app.app_context():  
            db.create_all() 
            cls.test_user = User(username='testuser', email='test@example.com', password_hash='testpassword') 
            cls.test_spot = Spot(name='Test Spot', latitude=37.7749, longitude=-122.4194) 
            db.session.add(cls.test_user)
            db.session.add(cls.test_spot) 
            db.session.commit() 

#Clean up after tests
    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
        cls.connection.close()
        cls.engine.dispose()

#Test the maps URL API
    def test_maps_url(self):
        response = self.client.get('/api/maps-url/37.7749/-122.4194')
        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.json)

#Tests weather data retrieval
    def test_get_weather_data(self):
        weather_data = get_weather_data(37.7749, -122.4194)
        self.assertIn('temperature', weather_data)

#Checks if user loading works correctly with ID
    def test_load_user(self):
        with self.app.app_context():
            user = load_user(self.test_user.user_id)
            self.assertEqual(user.username, 'testuser')

#Tests that the home page loads and contains expected spot name
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Spot', response.data)

#Verifies that the spot details page loads correctly
    def test_spot_details(self):
        response = self.client.get('/spot/1')  
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Spot', response.data)

#Tests login functionality
    def test_login(self):
        response = self.client.post('/login', data={'email': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)

#Tests logout functionality
    def test_logout(self):
        with self.client:
            login_user(self.test_user)
            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 302)

#Tests user registration
    def test_register_user(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)

#Tests saving a new spot
    def test_save_marker(self):
        response = self.client.post('/api/save-marker', json={
            'latitude': 37.7749,
            'longitude': -122.4194,
            'name': 'New Test Spot'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Marker saved successfully!', response.json['message'])

#Tests accessing the profile page after logging in
    def test_profile(self):
        with self.client:
            login_user(self.test_user)
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'testuser', response.data)

if __name__ == '__main__':
    unittest.main()
