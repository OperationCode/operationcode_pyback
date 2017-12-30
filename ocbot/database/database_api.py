from sqlalchemy import create_engine
from ocbot.database.models import Base, User, Interest
from sqlalchemy.orm import sessionmaker


class PyBotDatabase:
    def __init__(self, engine: str = 'sqlite:///memory'):
        self.engine = create_engine(engine)

    def remake_tables(self) -> None:
        """
        Drops and recreates User and Interests tables
        :return:
        """
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def _populate_interests(self) -> None:
        """
        Pre-populates the interests table
        """
        session = sessionmaker(bind=self.engine)()
        interests = ["Java", "Javascript", "Ruby", "Python", "C#", "HTML / CSS", "C", "Web Developer", "Web Designer",
                     "Front-End Developer", "Back-End Developer", "Full-Stack Developer", "Mobile / IOS",
                     "Mobile / Android",
                     "Cyber Security", "Data Science"]

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
        session = sessionmaker(bind=self.engine)()
        returned_interests = session.query(User).filter_by(**kwargs).first().interests
        return [interest.name for interest in returned_interests]

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
        session = sessionmaker(bind=self.engine)()
        res = session.add(User(**kwargs))
        session.commit()
        return res

    def update_user(self, email: str, **kwargs: dict) -> bool:
        """
        TODO: This will not handle appending new interests correctly

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
        session = sessionmaker(bind=self.engine)()
        num_records = session.query(User).filter_by(email=email).update({**kwargs})
        session.commit()
        return bool(num_records)

    def delete_user(self, email: str) -> bool:
        """
        Deletes the user with the given email from the users table
        :param email:
        :return boolean:
            Returns true if a record was successfully deleted
        """
        session = sessionmaker(bind=self.engine)()
        num_records = session.query(User).filter_by(email=email).delete()
        session.commit()
        return bool(num_records)


if __name__ == '__main__':
    db = PyBotDatabase()
    params = {
        'first_name': 'Bob',
        'last_name': 'Boberson',
        # 'email': 'fake@email.com'
    }
    num = db.update_user('fake@email.com', **params)
    # num = db.add_user(**params)
    print(num)
