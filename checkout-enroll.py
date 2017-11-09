from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

from sqlalchemy.sql import func

# import os

UDEMY_EMAIL = "REPLACE_ME" # replace this with your access key, for example: UDEMY_EMAIL = "your_email_address@blah.com"
# UDEMY_EMAIL = os.environ.get('UDEMY_EMAIL_ADDRESS')
UDEMY_PASSWORD = "REPLACE_ME" # replace this with your access key, for example: UDEMY_PASSWORD = "ilovecplusplus"
# UDEMY_PASSWORD = os.environ.get('UDEMY_PASSWORD')
UDEMY_FOLDER_PATH = "REPLACE_ME" # replace this with your access key, for example: UDEMY_FOLDER_PATH = "C:/Users/YOUR_USERNAME/udemy-selenium/"
# Windows users beware - change all \ to / in folder path
# UDEMY_FOLDER_PATH = os.environ.get('UDEMY_FOLDER_PATH')

# Initialise Database
engine = create_engine('sqlite:///courses.db')
Session = sessionmaker(bind=engine)
session = Session()

if session.query(Course).filter(Course.discounted_price == 0).filter(Course.remarks.isnot("enrolled")).count() == 0:
    print("no courses to enroll. summarising and quitting...\n")

else:
    UDEMY_FOLDER_PATH = UDEMY_FOLDER_PATH + "chromedriver.exe"
    driver = webdriver.Chrome(UDEMY_FOLDER_PATH)
    driver.get("https://www.udemy.com/join/login-popup/")
    assert "Udemy" in driver.title

    email_field = driver.find_element_by_id("id_email")
    email_field.clear()
    email_field.send_keys(UDEMY_EMAIL)

    password_field = driver.find_element_by_id("id_password")
    password_field.clear()
    password_field.send_keys(UDEMY_PASSWORD)

    try:
        email_field.send_keys(Keys.RETURN)
    except:
        wait = WebDriverWait(driver, 5)
        home_page = wait.until(EC.url_to_be("https://www.udemy.com/"))


    # start enrolling!
    # if discounted_price = 0  and remarks != enrolled
    print("initialising enrollment...")
    for checkout_tr in session.query(Course).filter(Course.discounted_price == 0).filter(Course.remarks.isnot("enrolled")):
        checkout_url = checkout_tr.checkout_url

        try:
            driver.get(checkout_url)
        except:
            WebDriverWait(driver, 10).until(lambda driver: driver.current_url != checkout_url)

        if "/cart/success/" in driver.current_url:
            driver.implicitly_wait(10) # just in case
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "success-lead__action")))
            print("successfully enrolled!")

            # update db
            checkout_tr.remarks = "enrolled"
            session.commit()
            print("row", str(checkout_tr.id), "updated\n")


        elif driver.current_url.endswith("/overview"):
            print("already enrolled. skipping to next...")

            # update db
            checkout_tr.remarks = "enrolled"
            session.commit()
            print("row", str(checkout_tr.id), "updated\n")

        else:
            print("an error has occured. skipping to next...")

    # Author's Remarks: you can remove "filter(Course.remarks.isnot("enrolled"))" to re-check all courses which are free.

    # last
    driver.close()
    print("all enrollment completed.\n")
