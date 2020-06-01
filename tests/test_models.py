from tests.basicstest import BasicTestCase
from models import User, Vocabularies

class TestUserModel(BasicTestCase):
    """Tests the User model"""
    def test_user(self):
        """Tests the User model variable"""
        user  = User(id = 1, username='Aname', password="pass")
        expected = {
            "id": 1,
            "username": "Aname",
            "password": "pass"
        }
        self.assertEqual(
            {
                "id": user.id,
                "username": user.username,
                "password": user.password
            }, 
            expected, 
            "one or more values in the dictionary is not equal"
                )

    def test_user_db_integration(self):
        """Tests User model with db integration"""
        with self.app_context():
            user  = User(username='Aname', password="pass")
            self.assertIsNone(user.query_by_username("Aname"), f"Query is not empty for the name: {user.username}")
            user.store_in_db()
            self.assertIsNotNone(user.query_by_username("Aname"), f"Query is empty for the name: {user.username}")
            user.delete_from_db()
            self.assertIsNone(user.query_by_username("Aname"), f"Query is not empty for the name: {user.username}")
    
class TestVocabulariesModel(BasicTestCase):
    """Tests the Vocabularies model"""
    def test_vocabularies_db_integration(self):
        with self.app_context():
            u = User(username='Aname', password="pass")
            v = Vocabularies(word="learn", sentence="we can learn by practice", voc=u)
            self.assertIsNone(v.find_by_word('learn'), f"Vocabulary is exist: {v.word}")
            v.store_in_db()
            self.assertIsNotNone(v.find_by_word('learn'), f"Vocabulary is not exist: {v.word}")
            self.assertEqual(v.voc.username, 'Aname') # testing relationship
            v.delete_from_db()
            self.assertIsNone(v.find_by_word('learn'), f"Vocabulary is exist: {v.word}")


            