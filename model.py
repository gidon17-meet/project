from sqlalchemy import Column, Boolean, Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context



Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(String)
    location = Column(String)
    invited = relationship("InvitesAssociation", back_populates="event")
    owner_id = Column(Integer, ForeignKey('member.id'))
    owner = relationship("Member", back_populates="my_events")

class Member(Base):
	__tablename__ = 'member'
	id = Column(Integer,primary_key=True)
	my_events=relationship("Event",back_populates="owner")
	name = Column(String)
	email = Column(String)
	password_hash = Column(String(255))
	events = relationship("InvitesAssociation",back_populates="member")

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)
    
class InvitesAssociation(Base):
    __tablename__ = 'invitesAssociation'
    member_id = Column(Integer, ForeignKey('member.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    attending = Column(Boolean)
    member = relationship("Member", back_populates="events")
    event = relationship("Event", back_populates="invited")


engine = create_engine('sqlite:///fizzBuzz.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()