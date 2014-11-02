from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime

Base = declarative_base()   #all model classes inherit from this class


class Deed(Base):
    __tablename__ = 'deeds'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    description = Column(Unicode(250), default='')
    good = Column(Boolean, default=None)

#class Email(Base):
#    __tablename__ = 'emails'
#
#    email = Column(Unicode(100), primary_key=True)
#    student_reg_no = Column(Unicode(100), ForeignKey(Student.registration_number))
#
#    student = relationship(Student, backref=backref('emails'))
