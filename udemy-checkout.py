import requests, urllib # , beautifulsoup4
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

import re
import datetime
now = datetime.datetime.now()
date_last_checked = datetime.datetime(now.year, now.month, now.day)

# Initialise Database
engine = create_engine('sqlite:///courses.db')
Session = sessionmaker(bind=engine)
session = Session()

for udemy_tr in session.query(Course).filter(Course.status == "udemy url found").filter(Course.post_date.isnot("reddit")):
    result = requests.get(udemy_tr.udemy_url)
    assert result.status_code != "200"

    try:
        soup = BeautifulSoup(result.content, "html.parser")

        # course_name
        sample = soup.find("h1", "clp-lead__title")
        course_name = sample.text
        print("course_name:", course_name)

        # checkout_url
        sample = soup.find("a", "course-cta--buy")
        checkout_url = "https://www.udemy.com" + sample.attrs['href']
        print("checkout_url:", checkout_url)

        # discounted_price
        sample = soup.find("span", "price-text__current")
        print("sample.text:", sample.text)

        if "Current price:" in sample.text:
            # i.e. Course was once paid, but now on discount (not necessarily free though)
            discounted_price = sample.text.split("Current price: ")[1].strip()
            print("old discounted_price:", discounted_price)
            if discounted_price == "Free":
                discounted_price = 0
            else:
                discounted_price = int(re.findall('\d+', discounted_price)[0])
            print("new discounted_price:", discounted_price)

            # original_price
            sample = soup.find("span", "price-text__old--price")
            original_price = sample.text.split("Original price: ")[1].strip()
            original_price = int(re.findall('\d+', original_price)[0])
            print("original_price:", original_price)

            # update db
            udemy_tr.course_name = course_name
            udemy_tr.checkout_url = checkout_url
            udemy_tr.original_price = original_price
            udemy_tr.discounted_price = discounted_price
            udemy_tr.status = "checkout url found"
            udemy_tr.date_last_checked = date_last_checked # date_last_checked = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
            session.commit()
            print("row", str(udemy_tr.id), "updated\n")


        elif "Price:" in sample.text:
            # i.e. Course is NOT on discount, price might be free or paid
            original_price = sample.text.split("Price: ")[0].strip()
            print("old original_price:", original_price)
            if "Free" in original_price:
                original_price = 0
            else:
                original_price = int(re.findall('\d+', original_price)[0])
            print("new original_price:", original_price)
            discounted_price = None
            print("discounted_price:", discounted_price)

            # update db
            udemy_tr.course_name = course_name
            udemy_tr.checkout_url = checkout_url
            udemy_tr.original_price = original_price
            udemy_tr.discounted_price = discounted_price
            udemy_tr.status = "checkout url found"
            udemy_tr.date_last_checked = date_last_checked # date_last_checked = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
            session.commit()
            print("row", str(udemy_tr.id), "updated\n")

        else:
            print("error has occured when retrieving price. skipping to next...\n")

    except:
        print("error, skipping row", str(udemy_tr.id), "to next...\n")
        pass
