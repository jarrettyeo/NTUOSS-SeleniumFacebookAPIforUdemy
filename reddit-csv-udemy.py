import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

# Initialise Database
engine = create_engine('sqlite:///courses.db')
Session = sessionmaker(bind=engine)
session = Session()

for line in open("reddit.csv"):
    udemy_url = line.strip()

    if session.query(Course).filter(Course.udemy_url == udemy_url).first() is not None:
        print("udemy url already added @ row", session.query(Course).filter(Course.udemy_url == udemy_url).first().id ,". skipping to next...")
    else:
        course = Course(bitly_url=None, post_date="reddit", status="udemy url found", expanded_url=None, udemy_url=udemy_url, checkout_url=None, course_name=None, discounted_price=None, original_price=None, date_last_checked=None, remarks=None)
        print("successfully added for udemy_url:", udemy_url)
        session.add(course)
    session.commit()

print("reddit import completed.")
