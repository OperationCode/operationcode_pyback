from sqlalchemy import create_engine
from ocbot.database.models import Base, User, Interest, UserGroup
from sqlalchemy.orm import sessionmaker, Session


class PyBotDatabase:
    def __init__(self, engine: str = 'sqlite:///memory'):
        self.engine = create_engine(engine, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def remake_tables(self) -> None:
        """
        Drops and recreates User and Interests tables
        """
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def _populate_interests(self) -> None:
        """
        Pre-populates the interests table
        """
        session = self.Session()
        interests = ["Javascript", "Ruby", "Java", "Python", "C#", "C", "Swift", ".NET", "HTML / CSS", "Mobile / IOS",
                     "Full-Stack Developer", "Data Science", "Back-End Developer", "Front-End Developer",
                     "Cyber Security", "I.T / SysAdmin", "Web Designer", "Web Developer", "Mobile / Android"]

        for interest in interests:
            session.add(Interest(name=interest))

        session.commit()

    def get_user_interests(self, **kwargs: dict) -> list:
        """
        :param kwargs:
            Accepts a variable number of query parameters as kwargs
        :return
            Returns a list of the returned interests as strings
        """
        session = self.Session()
        interests = session.query(User).filter_by(**kwargs).first().interests
        return [interest.name for interest in interests]

    def add_user(self, **kwargs: dict) -> None:
        """
        Adds a new user to the table.
        Fields should be supplied in the form of a dict
        e.g.::
            {
            'first_name': 'Bob',
            'last_name': 'Boberson'
            'email': 'fake@email.com'
            }

        The email argument is REQUIRED
        :param kwargs:
        """
        session = self.Session()
        interests = kwargs.pop('interests', None)
        new_user = User(**kwargs)
        res = session.add(new_user)
        if interests:
            new_user.interests = session.query(Interest).filter(Interest.name.in_(interests)).all()
        session.commit()
        return res

    def update_user(self, email: str, **kwargs: dict) -> bool:
        """
        Updates a user with the given email in the users table
        Fields to be updated should be given in the form of a dict
        e.g.::
            {
            'first_name': 'Bob',
            'last_name': 'Boberson'
            }

        :param email:
        :param kwargs:
        :return boolean:
            Returns true if a record was successfully updated
        """
        session = self.Session()
        user = session.query(User).filter_by(email=email).first()
        interests = kwargs.pop('interests', None)

        res = False
        if kwargs:
            res = user.update({**kwargs})
        if interests is not None:
            #  queries the Interest table for all rows with names matching those in the list,
            #  collects them into a new list of Interest objects, and assigns that list to the user
            user.interests = session.query(Interest).filter(Interest.name.in_(interests)).all()
            res = True
        session.commit()
        return bool(res)

    @staticmethod
    def _handle_interests(user: User, session: Session, interests: list) -> bool:
        """
        Utility method for assigning a list of interests to User object

        :param user:
        :param session:
        :param interests:
        """
        interest_list = session.query(Interest).filter(Interest.name.in_(interests)).all()
        user.interests = interest_list
        return True

    def delete_user(self, email: str) -> bool:
        """
        Deletes the user with the given email from the users table
        :param email:
        :return boolean:
            Returns true if a record was successfully deleted
        """
        session = self.Session()
        res = session.query(User).filter_by(email=email).delete()
        session.commit()
        return bool(res)

    def assign_usergroup(self, email: str, group: str) -> bool:
        """
        Parses the UserGroup value of the given string and assigns the user
        to that group.
        :param email:
        :param group:
        :return boolean:
            Returns true if user is found and assigned to new UserGroup
        """
        session = self.Session()
        res = session.query(User).filter_by(email=email)
        if not res.first() or group not in UserGroup.__members__:
            return False

        res.first().usergroup = UserGroup[group]
        session.commit()
        return True


if __name__ == '__main__':
    """
    Stuff for lazy testing.
    """
    db = PyBotDatabase()
    db.remake_tables()
    db._populate_interests()

    params = {
        'first_name': 'Bob',
        'last_name': 'Boberson',
        'interests': ['Java', 'Ruby'],
        'email': 'fake@email.com',
    }
    db.add_user(**params)

    search_kwargs = {'email': 'fake@email.com'}
    print(db.get_user_interests(**search_kwargs))

    new_kwargs = {'interests': ['Python']}
    db.update_user('fake@email.com', **new_kwargs)
    print(db.get_user_interests(**search_kwargs))
