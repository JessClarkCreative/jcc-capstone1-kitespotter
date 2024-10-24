import unittest
from app import app, db, User, Spot, load_user, get_weather_data
from flask_login import login_user
from werkzeug.security import generate_password_hash
import os

class KiteSpotAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'postgresql://user:password@localhost/test_db')
        
        cls.client = cls.app.test_client()
        
        with cls.app.app_context():
            db.create_all()
            cls.test_user = User(username='testuser', email='test@example.com', password_hash=generate_password_hash('testpassword'))
            cls.test_spot = Spot(name='Test Spot', latitude=37.7749, longitude=-122.4194)
            db.session.add(cls.test_user)
            db.session.add(cls.test_spot)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        # Reset the session or perform any setup before each test if needed
        pass

    def tearDown(self):
        # Clean up after each test if necessary
        pass

    # def test_register_user(self):
    #     """PASSING Test user registration."""
    #     response = self.client.post('/register', data={
    #         'username': 'newuser',
    #         'email': 'newuser@example.com',
    #         'password': 'newpassword'
    #     })
    #     self.assertEqual(response.status_code, 302)  # Check for redirect on successful registration
    #     with self.app.app_context():
    #         user = User.query.filter_by(username='newuser').first()
    #         self.assertIsNotNone(user)

    # def test_login(self):
    #     """PASSING Test the login functionality."""
    #     response = self.client.post('/login', data={'email': 'test@example.com', 'password': 'testpassword'})
    #     self.assertEqual(response.status_code, 302)  # Check for redirect on successful login

    # def test_load_user(self):
    #     """Test loading a user by ID."""
    #     with self.app.app_context():
    #         user = User.query.get(self.test_user.user_id)
    #         self.assertIsNotNone(user)
    #         self.assertEqual(user.email, 'test@example.com')

    # def test_logout(self):
    #     """Tests logout functionality"""
    #     with self.app.app_context():
    #         login_user(self.test_user)
    #         response = self.client.get('/logout')
    #         self.assertEqual(response.status_code, 302)

    # def test_home_page(self):
    #     """PASSING Test that the home page loads correctly."""
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Test Spot', response.data)  # Check for expected content

    # def test_spot_details(self):
    #     """PASSING Test that the spot details page loads correctly."""
    #     response = self.client.get('/spot/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Test Spot', response.data)

    # def test_maps_url(self):
    #     """PASSING Test the maps URL API"""
    #     latitude = 37.7749
    #     longitude = 122.4194
    #     response = self.client.get(f'/api/maps-url/{latitude}/{longitude}')
    #     print (response.get_data(as_text=True))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('url', response.json)
            
    # def test_get_weather_data(self):
    #     """PASSING Tests weather data retrieval"""
    #     weather_data = get_weather_data(37.7749, -122.4194)
    #     self.assertIn('temperature', weather_data)

    # def test_save_marker(self):
    #     """PASSING Tests saving a new spot"""
    #     response = self.client.post('/api/save-marker', json={
    #         'latitude': 37.7749,
    #         'longitude': -122.4194,
    #         'name': 'New Test Spot'
    #     })
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn('Marker saved successfully!', response.json['message'])
            

if __name__ == '__main__':
    unittest.main()
