from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

engine = create_engine('sqlite:///courses.db', echo=True)
Base = declarative_base()

class Course(Base):

    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    bitly_url = Column(String, default=None, index=True)
    post_date = Column(String, default=None, index=True)
    expanded_url = Column(String, default=None, index=True)
    udemy_url = Column(String, default=None, index=True)
    checkout_url = Column(String, default=None, index=True)
    course_name = Column(String, default=None, index=True)
    discounted_price = Column(Integer, default=None, index=True)
    original_price = Column(Integer, default=None, index=True)
    date_last_checked = Column(Date, default=None, index=True)
    status = Column(String, default=None, index=True)
    remarks = Column(String, default=None, index=True)

    #----------------------------------------------------------------------
    def __init__(self, bitly_url, post_date, expanded_url, udemy_url, checkout_url, course_name, discounted_price, original_price, date_last_checked, status, remarks):

        self.bitly_url = bitly_url
        self.post_date = post_date
        self.expanded_url = expanded_url
        self.udemy_url = udemy_url
        self.checkout_url = checkout_url
        self.course_name = course_name
        self.discounted_price = discounted_price
        self.original_price = original_price
        self.date_last_checked = date_last_checked
        self.status = status
        self.remarks = remarks

# create tables
Base.metadata.create_all(engine)
