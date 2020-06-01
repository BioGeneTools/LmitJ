from tests.basicstest import BasicTestCase
from models import User, Vocabularies

class TestAuthentication(BasicTestCase):
    """Tests the auth endpoints"""
    def test_register(self):
        """Tests the registration endpoint"""
        with self.app() as client:
            with self.app_context():
                response = client.post('/v1.0/auth/register', data={"username": "Aname", "password": "Pass"})
                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(response.get_json(), {"message": "new user has been successfully registered"})
                self.assertIsNotNone(User.query_by_username("Aname"))

    def test_auth(self):
        """Tests the auth endpoint"""
        with self.app() as client:
            with self.app_context():
                client.post('/v1.0/auth/register', 
                    data={"username": "Aname", "password": "Pass"})
                response = client.post('/v1.0/auth', 
                    data={"username": "Aname", "password": "Pass_wrong"}, 
                    headers={'Contet-Type': 'application/json'})
                self.assertEqual(response.status_code, 401)
                self.assertEqual(response.get_json(), {"message": "Bad username or password"})
                response = client.post('/v1.0/auth', 
                    data={"username": "Aname", "password": "Pass"}, 
                    headers={'Contet-Type': 'application/json'})
                self.assertEqual(response.status_code, 200)
                self.assertIn('access_token', response.get_json())
    
    

