from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
import enum

Base = declarative_base()

#  un-mapped Table construct serves as the association table between
#  users and interests
interest_associations = Table('interest_associations', Base.metadata,
                              Column('user_id', Integer, ForeignKey('users.id')),
                              Column('interest_id', Integer, ForeignKey('interests.id')),
                              )


class UserGroup(enum.Enum):
    Contributor = 0
    Leadership = 1
    Mentor = 2
    Default = 3


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50), nullable=False, unique=True)
    interests = relationship('Interest', secondary=interest_associations,
                             back_populates='users')
    usergroup = Column(ChoiceType(UserGroup, impl=Integer()), default=UserGroup.Default.value)

    def __repr__(self) -> str:
        return f'{self.id} | {self.first_name} | {self.last_name} | {self.email} | {self.interests}'


class Interest(Base):
    __tablename__ = 'interests'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    users = relationship('User', secondary=interest_associations,
                         back_populates='interests')

    def __repr__(self):
        return self.name
