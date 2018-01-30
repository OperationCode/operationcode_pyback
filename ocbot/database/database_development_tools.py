from ocbot.database.pybotdatabase import PyBotDatabase
from ocbot.keys import PG_USERNAME, PG_PASSWORD, PA_SSH_PASSWORD, PA_SSH_URL, PA_SSH_USERNAME, \
    PA_SSH_REMOTE_BIND_ADDR, PA_SSH_REMOTE_BIND_PORT

from sshtunnel import SSHTunnelForwarder


def _pa_postgres_testing():
    """
    Tunneling is necessary when connecting to PythonAnywhere Postgresql server when running locally
    """
    with SSHTunnelForwarder(
            (PA_SSH_URL, 22),  # Remote server IP and SSH port
            ssh_username=PA_SSH_USERNAME,
            ssh_password=PA_SSH_PASSWORD,
            remote_bind_address=(PA_SSH_REMOTE_BIND_ADDR, PA_SSH_REMOTE_BIND_PORT),  # IP Addr/Port of postgres server
    ) as server:
        print('Server connected via ssh')
        db = PyBotDatabase(
            f'postgresql+psycopg2://{PG_USERNAME}:{PG_PASSWORD}@127.0.0.1:{server.local_bind_port}/octest', echo=True)

        db._remake_tables()
        db._populate_interests()

        print('interests populated')

        db.add_user(**TEST_USER_1)
        db.assign_usergroup(email='fake@email.com', group='Leadership')

        print(db.get_user('fake@email.com'))  # 1 | Billy | Boberson | fake@email.com | [Java, Python]
        db.close_all()


def _docker_postgres_testing():
    db_conf = {
        'ENGINE': 'postgresql',
        'database': 'postgres',
        'user': 'postgres',
        'pass': 'secret',
        'host': 'localhost',
        'port': 5432,
    }

    engine = f"postgresql+psycopg2://" \
             f"{db_conf['user']}:{db_conf['pass']}@{db_conf['host']}:{db_conf['port']}/{db_conf['database']}"
    db = PyBotDatabase(engine, echo=True)

    db._remake_tables()
    db._populate_interests()
    #
    # print('interests populated')
    #
    # db.add_user(**TEST_USER_1)
    # db.assign_usergroup(email='fake@email.com', group='Leadership')
    #
    # print(db.get_user('fake@email.com'))  # 1 | Billy | Boberson | fake@email.com | [Java, Python]
    db.close_all()


def _in_memory_sqlite_testing():
    db = PyBotDatabase()
    db._remake_tables()
    db._populate_interests()
    db.add_user(**TEST_USER_1)
    db.add_user(**TEST_USER_1)
    # params['email'] = 'fake2@email.com'
    # db.add_user(**params)
    # db.assign_usergroup(email='fake@email.com', group='Leadership')
    # print(db.get_user('fake@email.com'))  # 1 | Billy | Boberson | fake@email.com | [Java, Python]
    # print(db.get_user('fake2@email.com'))  # 1 | Billy | Boberson | fake@email.com | [Java, Python]

    # user = db.get_user('fake@email.com')
    # print(user.__dict__)

    db.close_all()


TEST_USER_1 = {'first_name': 'Billy', 'last_name': 'Boberson', 'interests': ['Java', 'Python'],
               'email': 'fake@email.com', }