from enum import unique
import string
from turtle import title
from unicodedata import name
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
import sys

from .database import Base

email_to = Table('email_to', Base.metadata,
Column('email_id', ForeignKey('emails.id'), primary_key=True),
Column('person_id', ForeignKey('persons.id'), primary_key=True)
)

class Folder(Base):
    __tablename__= "folders"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    icon = Column(String)

class Person(Base):
    __tablename__ = "persons"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    avatar = Column(String)

class Email(Base):
    __tablename__ = "emails"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, index=True)
    froms_id = Column(Integer,ForeignKey("persons.id"))
    froms = relationship("Person")
    to = relationship("Person", secondary=email_to)
    subject = Column(String)
    message = Column(String)
    time = Column(String)
    read = Column(Boolean)
    starred = Column(Boolean)
    important = Column(Boolean)
    hasAttachments = Column(Boolean)
    #labels = Column(String)

    attachments = relationship("Attachments", back_populates = "referring_Email")

class Attachments(Base):
    __tablename__ = "attachments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    type = Column(String)
    fileName = Column(String)
    preview = Column(String)
    url = Column(String)
    size = Column(String)
    email_id = Column(String, ForeignKey("emails.id"))

    referring_Email = relationship("Email", back_populates = "attachments")
