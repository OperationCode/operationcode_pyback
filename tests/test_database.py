# import unittest
# from tests.posgresql import Postgresql
#
# from ocbot.database.pybotdatabase import PyBotDatabase
#
# TEST_USER_1 = {'first_name': 'Billy', 'last_name': 'Boberson', 'interests': ['Ruby', 'Python'],
#                'email': 'fake@email.com', }
# TEST_USER_2 = {'first_name': 'Bobby', 'last_name': 'Boberson', 'interests': ['Java', 'Python'],
#                'email': 'fake2@email.com', }
#
#
# class TestAddUsers(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         """
#         One-time setup for spinning up postgres database
#         """
#         super(TestAddUsers, cls).setUpClass()
#         cls.mock_db = Postgresql()
#         db_conf = cls.mock_db.dsn()
#
#         engine = f"postgresql+psycopg2://" \
#                  f"{db_conf['user']}@{db_conf['host']}:{db_conf['port']}/{db_conf['database']}"
#
#
#         cls.db = PyBotDatabase(engine)
#
#     def setUp(self):
#         self.db._remake_tables()
#         self.db._populate_interests()
#
#     def tearDown(self):
#         self.db.close_all()
#
#     def test_add_user_returns_true_when_valid(self):
#         res = self.db.add_user(**TEST_USER_1)
#
#         self.assertTrue(res, "add_user returned false")
#
#         # TODO: Move this to a TestSearch class
#         user = self.db.get_user('fake@email.com')
#
#         for key, val in TEST_USER_1.items():
#             if key == 'interests':
#                 continue
#             self.assertEquals(user.__dict__[key], val)
#
#     def test_add_user_returns_false_when_duplicate(self):
#         self.assertTrue(self.db.add_user(**TEST_USER_1), 'First add did not return true')
#         self.assertFalse(self.db.add_user(**TEST_USER_1), 'Duplicate add did not return false')
#         self.assertFalse(self.db.add_user(**TEST_USER_1), 'Duplicate add did not return false')
#
#     def test_add_user_can_add_valid_user_after_adding_invalid(self):
#         self.assertTrue(self.db.add_user(**TEST_USER_1), 'First add did not return true')
#         self.assertFalse(self.db.add_user(**TEST_USER_1), 'Duplicate add did not return false')
#         self.assertTrue(self.db.add_user(**TEST_USER_2), 'Duplicate add did not return false')
#
#     def test_add_multiple_users(self):
#         self.assertTrue(self.db.add_user(**TEST_USER_1))
#         self.assertTrue(self.db.add_user(**TEST_USER_2))
