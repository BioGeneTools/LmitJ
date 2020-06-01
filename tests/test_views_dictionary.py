from tests.basicstest import BasicTestCase
from models import User, Vocabularies

class TestDictionary(BasicTestCase):
    """Tests the dictionary endpoints"""
    def test_dict(self):
        with self.app() as client:
            with self.app_context():
                client.post('/v1.0/auth/register', 
                    data={"username": "Aname", "password": "Pass"})
                response_auth = client.post('/v1.0/auth', data={"username": "Aname", "password": "Pass"})
                response = client.get('/v1.0/dict', headers={'Authorization': f'Bearer {response_auth.get_json()["access_token"]}'})
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(response.get_json(), {"message": "your dictionary is empty"})
