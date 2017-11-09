import urllib.request
import json
import re

import itertools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

# import os

FACEBOOK_KEY = "REPLACE_ME" # replace this with your access key, for example: FACEBOOK_KEY = "1234567890|sdubgfownudgwer28ru8nc"
# FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY')
url = "https://graph.facebook.com/v2.2/546443732093598/posts?access_token=" + FACEBOOK_KEY + "&limit=100"

try:
    r = urllib.request.urlopen(url)
except urllib.error.HTTPError:
    # raise
    print("Error retrieving page. Quitting Python...")
    quit()

data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

try:
    print("page 0 exists.")
    print(url, "\n")
    print(data["paging"]["next"], "\n")
except (AttributeError, KeyError):
    print("No data found.")
    quit()

# Initialise Database
engine = create_engine('sqlite:///courses.db')
Session = sessionmaker(bind=engine)
session = Session()

for page_count in itertools.count(1): # count(start, [step]) -> https://docs.python.org/3/library/itertools.html
    try:
        url = "https://graph.facebook.com/v2.2/546443732093598/posts?access_token=" + FACEBOOK_KEY + "&limit=100" + "&offset=" + str(page_count) + "00"
        r = urllib.request.urlopen(url)
        data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

        ## START STEP 2 ##
        ########################################################################################
        for key in data["data"]:
            try:
                bitly_url = re.search("(?P<url>https?://bit.ly[^\s]+)", key["message"]).group("url")
                post_date = key["created_time"]
                print(bitly_url, "\n", post_date)

                # if bitly_url and post_date exist, then pass (for the first time, thereafter quit <- we are NOT doing this in this workshop)
                # else if bitly_url exist but post_date does not exist, do not add and pass
                # else, add entry into db.

                if session.query(Course).filter(Course.bitly_url == bitly_url).filter(Course.post_date == post_date).first() is not None:

                    # uncomment below if this is the first time scrapping this Facebook page
                    print("bit.ly url and post date duplicate found @", session.query(Course).filter(Course.bitly_url == bitly_url).filter(Course.post_date == post_date).first().post_date ,"so skipping to next...")
                    pass

                    # uncomment below if you have scrapped all of this Facebook page
                    # print("bit.ly url and post date duplicate found. quitting python...")
                    # quit()

                elif session.query(Course).filter(Course.bitly_url == bitly_url).first() is not None:
                    print("bit.ly url already added @", session.query(Course).filter(Course.bitly_url == bitly_url).first().post_date ,". skipping to next...")
                    pass

                else:
                    course = Course(bitly_url=bitly_url, post_date=post_date, status="bit.ly url found", expanded_url=None, udemy_url=None, checkout_url=None, course_name=None, discounted_price=None, original_price=None, date_last_checked=None, remarks=None)
                    session.add(course)
                    session.commit()
                    print("bit.ly url added!")

            except AttributeError:
                pass

        ########################################################################################
        ## END STEP 2 ##

        print("page", str(page_count), "exists.")
        print(url, "\n")
        print(data["paging"]["next"], "\n")
    except KeyError:
        print("No additional data found.")
        session.close()
        quit()
