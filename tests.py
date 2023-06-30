import unittest
from server import app

class FlaskAppTests (unittest.TestCase):
    """Tests for the heat resilience app"""

    def setUp(self):
        """Set up before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_show_homepage(self):
        """Test that homepage HTML renders."""
        
        result = self.client.get('/')
        self.assertIn(b'<h4>Create an Account</h4>', result.data)

    
    def test_create_user(self):
        """Test that a user is created with correct data types."""

        # result = self.client.post("/users",
        #          data={
        #         "fname": "Tabitha",
        #         "city": "Fargo",
        #         "country_code": "US",
        #         "phone": 555-555-8888,
        #         "email": tab@test.xyz,
        #  

        #           },

        #           follow_redirects=True)

        # self.assertIn(b"Your account was created successfully! You can now log in.", result.data)


if __name__ == '__main__':
    # If called like a script, run the tests
    unittest.main()
