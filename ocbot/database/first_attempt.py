from sqlalchemy import create_engine
from ocbot.database.models import Base, User, Interest
from sqlalchemy.orm import sessionmaker


def make_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def populate_tables():
    Session = sessionmaker(bind=engine)
    session = Session()
    #  Create our first user and add them to the users table
    allen = User(first_name='Allen', last_name='Anthes', email='fake@email.com')
    session.add(allen)
    session.commit()

    #  User object returned from the table
    our_user = session.query(User).filter_by(first_name='Allen').first()

    #  I figure this will be supplied as an param of the method call
    interests = ['Java', 'Ruby']
    for interest in interests:
        #  Get the associated Interest object from interests table, then append them to the users interests
        #  TODO: There is probably a better way to do this when we do this for real and
        #  TODO: we're receiving new users from the API
        interest_object = session.query(Interest).filter_by(name=interest).first()
        our_user.interests.append(interest_object)

    session.commit()

    updated_user = session.query(User).filter_by(first_name='Allen').first()
    print(updated_user)  # 1 | Allen | Anthes | fake@email.com | [1 | Java, 3 | Ruby]


def make_interests():
    """
    Pre-populates the interests table
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    interests = ["Java", "Javascript", "Ruby", "Python", "C#", "HTML / CSS", "C", "Web Developer", "Web Designer",
                 "Front-End Developer", "Back-End Developer", "Full-Stack Developer", "Mobile / IOS",
                 "Mobile / Android",
                 "Cyber Security", "Data Science"]

    for interest in interests:
        session.add(Interest(name=interest))

    session.commit()


if __name__ == '__main__':
    engine = create_engine('sqlite:///memory', echo=True)
    # make_tables()
    populate_tables()
    # make_interests()
