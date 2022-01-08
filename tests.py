import unittest
import crud, server, alert
from server import app

class FlaskAppTests (unittest.TestCase):
    """Tests for the heat resilience app"""

    def setUp(self):
        """Set up before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        """Tear down after each test."""


    def test_show_homepage(self):
        """Test that homepage HTML renders."""
        
        result = self.client.get('/')
        self.assertIn(b'<h4>Create an Account</h4>', result.data)
    
    def test_create_account(self):

        result = self.client.post('/users', data={
            'fname': 'blue',
            'city': 'city',
            'country_code': 'country_code',
            'phone': 'phone',
            'email': 'email',
            'password': 'password',
            'opted_in': 'opted_in',
            })
        self.assertTrue(result.data)

if __name__ == '__main__':
    # If called like a script, run the tests
    unittest.main()
