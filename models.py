from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean, Date, cast
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date, timedelta

Base = declarative_base()   #all model classes inherit from this class


class Deed(Base):
    __tablename__ = 'deeds'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    description = Column(Unicode(250), default='')
    good = Column(Boolean, default=None)

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


#class Email(Base):
#    __tablename__ = 'emails'
#
#    email = Column(Unicode(100), primary_key=True)
#    student_reg_no = Column(Unicode(100), ForeignKey(Student.registration_number))
#
#    student = relationship(Student, backref=backref('emails'))
