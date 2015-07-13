from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean  #, Date, cast
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship, backref
from datetime import datetime, timedelta
import json

from db import get_db_session

Base = declarative_base()   #all model classes inherit from this class



class Deed(Base):
    __tablename__ = 'deeds'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    description = Column(Unicode(250), default=u'')
    good = Column(Boolean, default=None)
    synced = Column(Boolean, default=False)

    def to_dict(self):
        return {'id': self.id,
                'timestamp': str(self.timestamp),
                'description': self.description,
                'good': self.good,
                'synced': self.synced}
    
    @classmethod
    def from_dict(cls, deed_dict):
        new_rec = cls(
            description=deed_dict['description'],
            good=deed_dict['good'],
            synced=True
        )
        new_rec.timestamp = datetime.strptime(deed_dict['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        
        return new_rec

    @classmethod
    def get_gb_count(cls, conn, start_date=None, end_date=None):
        "Return count of good and bad deeds for a given date or date range"

        if not start_date:
            good_count = conn.query(cls).filter_by(good=True).count()
            bad_count = conn.query(cls).filter_by(good=False).count()

            return good_count, bad_count

        if not end_date:
            end_date = start_date

        end_date += timedelta(days=1)

        good_count = conn.query(cls).filter_by(good=True).filter(
            Deed.timestamp >= start_date).filter(
            Deed.timestamp <= end_date).count()
        bad_count = conn.query(cls).filter_by(good=False).filter(
            Deed.timestamp >= start_date).filter(
            Deed.timestamp <= end_date).count()

        return good_count, bad_count

class Setting(Base):
    "Table to hold RPi Configration"
    
    __tablename__ = 'settings'

    key = Column(Unicode(200), primary_key=True)
    value = Column(Unicode(500))

    @classmethod
    def get(cls, key, default_val=None, db=None):
        "Get a key's value from DB or if not found return provided default value"

        if not db:
            db = get_db_session()

        rec = db.query(cls).filter_by(key=key).first()
        if rec:
            return rec.value
        else:
            return default_val
    
    @classmethod
    def set(cls, key, val, db=None):
        "Set a key's value"
        if not db:
            db = get_db_session()

        rec = db.query(cls).filter_by(key=key).first()
        if rec:
            rec.value = val
        else:
            rec = cls(key=key, value=val)
            db.add(rec)

    @classmethod
    def get_all(cls, db=None):
        "Return all settings as a dict"
        
        if not db:
            db = get_db_session()

        ret = {}
        for rec in db.query(cls):
            ret[rec.key] = rec.value

        return ret

#class Email(Base):
#    __tablename__ = 'emails'
#
#    email = Column(Unicode(100), primary_key=True)
#    student_reg_no = Column(Unicode(100), ForeignKey(Student.registration_number))
#
#    student = relationship(Student, backref=backref('emails'))
