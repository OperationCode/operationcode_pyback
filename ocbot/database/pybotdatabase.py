import json
from contextlib import contextmanager
from collections import namedtuple
from sqlalchemy import create_engine
from ocbot.database.models import Base, User, Interest, UserGroup
from sqlalchemy.orm import sessionmaker, Session

from ocbot.database.database_decorators import validate_integrity


class PyBotDatabase:
    def __init__(self, engine: str = 'sqlite:///memory', echo: bool = False):

        self.engine = create_engine(engine, echo=echo)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _remake_tables(self) -> None:
        """
        Drops and recreates User and Interests tables
        """
        Base.metadata.bind = self.engine
        Base.metadata.drop_all()
        Base.metadata.create_all()

    def _drop_users(self) -> None:
        User.__table__.drop(self.engine)
        User.__table__.create(self.engine)

    def _populate_interests(self) -> None:
        """
        Pre-populates the interests table
        Ideally this will eventually be pulled from OC backend
        """
        with self.session_scope() as session:
            interests = ["Javascript", "Ruby", "Java", "Python", "C#", "C", "Swift", ".NET", "HTML / CSS",
                         "Mobile / IOS",
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
        with self.session_scope() as session:
            interests = session.query(User).filter_by(**kwargs).first().interests
            res = [interest.name for interest in interests]
            session.close_all()
            return res

    @validate_integrity
    def add_user(self, **kwargs: dict) -> bool:
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
        with self.session_scope() as session:
            interests = kwargs.pop('interests', None)
            new_user = User(**kwargs)
            session.add(new_user)
            if interests:
                new_user.interests = session.query(Interest).filter(Interest.name.in_(interests)).all()
                session.commit()
            return True

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
        with self.session_scope() as session:
            user = session.query(User).filter_by(email=email).first()
            interests = kwargs.pop('interests', None)
            res = False
            if kwargs:
                res = user.update({**kwargs})
            if interests is not None:  # Checking for None allows us to pass in an empty list and reset interests

                #  queries the Interest table for all rows with names matching those in the list,
                #  collects them into a new list of Interest objects, and assigns that list to the user
                user.interests = session.query(Interest).filter(Interest.name.in_(interests)).all()
                res = True
            session.commit()
            return bool(res)

    def get_user(self, email: str) -> User:
        session = self.Session()
        user = session.query(User).filter_by(email=email).first()
        return session.query(User).get(user.id)

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
        with self.session_scope() as session:
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
        with self.session_scope() as session:
            res = session.query(User).filter_by(email=email)
            if not res.first() or group not in UserGroup.__members__:
                return False

            res.first().usergroup = UserGroup[group]
            session.commit()
            return True

    def close_all(self) -> None:
        """
        Utility function to close all open sessions
        """
        self.Session.close_all()

    @staticmethod
    def make_response(status: bool, key: int = None, body=None) -> dict:
        Response = namedtuple('Response', 'status key body')

        res = Response(status, key, body)

        res = json.dumps({
            'status': status,
            'key': key,
            'body': body
        })
        return res


if __name__ == '__main__':
    """
    Stuff for lazy testing.
    """


