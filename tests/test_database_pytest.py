from tests.posgresql import Postgresql
from ocbot.database.pybotdatabase import PyBotDatabase

TEST_USER_1 = {'first_name': 'Billy', 'last_name': 'Boberson', 'interests': ['Ruby', 'Python'],
               'email': 'fake@email.com', }
TEST_USER_2 = {'first_name': 'Bobby', 'last_name': 'Boberson', 'interests': ['Java', 'Python'],
               'email': 'fake2@email.com', }

mock_db = Postgresql()
db_conf = mock_db.dsn()

engine = f"postgresql+psycopg2://" \
         f"{db_conf['user']}@{db_conf['host']}:{db_conf['port']}/{db_conf['database']}"

db = PyBotDatabase(engine)


def setup_function(function):
    db._remake_tables()
    db._populate_interests()


def teardown_module(module):
    mock_db.terminate()


def teardown_function(function):
    db.close_all()


def test_add_user_returns_true_when_valid():
    res = db.add_user(**TEST_USER_1)

    assert res

    # TODO: Move this to a TestSearch class
    user = db.get_user('fake@email.com')

    for key, val in TEST_USER_1.items():
        if key == 'interests':
            continue
        assert user.__dict__[key] == val


def test_add_user_returns_false_when_duplicate():
    assert db.add_user(**TEST_USER_1)
    assert not db.add_user(**TEST_USER_1)
    assert not db.add_user(**TEST_USER_1)


def test_add_user_can_add_valid_user_after_adding_invalid():
    assert db.add_user(**TEST_USER_1)
    assert not db.add_user(**TEST_USER_1)
    assert db.add_user(**TEST_USER_2)
