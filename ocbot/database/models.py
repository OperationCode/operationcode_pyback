from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

#  un-mapped Table construct serves as the association table between
#  users and interests
interest_associations = Table('interest_associations', Base.metadata,
                              Column('user_id', ForeignKey('users.id'), primary_key=True),
                              Column('interest_id', ForeignKey('interests.id'), primary_key=True),
                              )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50), nullable=False)
    interests = relationship('Interest', secondary=interest_associations,
                             back_populates='users')

    def __repr__(self) -> str:
        return f'{self.id} | {self.first_name} | {self.last_name} | {self.email} | {self.interests}'


class Interest(Base):
    __tablename__ = 'interests'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    users = relationship('User',
                         secondary=interest_associations,
                         back_populates='interests')

    def __repr__(self):
        return f'{self.id} | {self.name}'
