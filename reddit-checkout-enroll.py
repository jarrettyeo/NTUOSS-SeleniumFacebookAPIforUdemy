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

# first, let's do a quick check if there are even courses for us to enroll in itfp.
# there are 3 main criteria that we need to look at:
# 1. it should not be already enrolled - .filter(Course.remarks.isnot("enrolled"))
# 2. it should come from reddit - .filter(Course.post_date == "reddit")
# 3. it should be a 0-dollar discounted price course
# if the total number (count) of this query is zero, it means there are no such courses for us to enroll in.
# else, we proceed with the work process.
if session.query(Course).filter(Course.discounted_price == 0).filter(Course.remarks.isnot("enrolled")).filter(Course.post_date == "reddit").count() == 0:
    print("no courses to enroll from reddit. summarising and quitting...\n")

else:
    UDEMY_FOLDER_PATH = UDEMY_FOLDER_PATH + "chromedriver.exe"
    driver = webdriver.Chrome(UDEMY_FOLDER_PATH)
        driver.get("https://www.udemy.com/join/login-popup/")

    # when you assert something, you tell the program to test if the condition is true.
    # if it isn't (i.e. condition is false), trigger an error.
    assert "Udemy" in driver.title

    # we find the email field here.
    email_field = driver.find_element_by_id("id_email")
    email_field.clear() # we clear the field just in case
    email_field.send_keys(UDEMY_EMAIL)

    # we find the password field here.
    password_field = driver.find_element_by_id("id_password")
    password_field.clear() # we clear the field just in case
    password_field.send_keys(UDEMY_PASSWORD)

    # in Selenium, it is common to use the try-except block to try navigating to a new page.
    # if it isn't successful (usually a timeout error will be thrown, i.e. page taking too long to load),
    # the program will exit try and execute the code under except.
    try:
        # lazy way of logging in by hitting enter.
        # alternatively, you could find the "Sign In" button and use the click function.
        email_field.send_keys(Keys.RETURN)
    except:
        wait = WebDriverWait(driver, 10)
        # EC is the Expected Condition that we are looking out for.
        # in this case, we are looking out for when the URl changes to udemy.com,
        # thereby indicating that you have successfully logged in.
        # of course that it is not the only way to check if you have logged in successfully.
        home_page = wait.until(EC.url_to_be("https://www.udemy.com/"))


    # let's start enrolling!
    print("initialising enrollment for reddit...")

    # we create a query to check for all courses with discounted_price = 0  and remarks != enrolled
    for checkout_tr in session.query(Course).filter(Course.discounted_price == 0).filter(Course.remarks.isnot("enrolled")).filter(Course.post_date == "reddit"):
        checkout_url = checkout_tr.checkout_url

        try:
            driver.get(checkout_url)
        except:
            WebDriverWait(driver, 10).until(lambda driver: driver.current_url != checkout_url)

        if "/cart/success/" in driver.current_url:
            driver.implicitly_wait(10) # just in case
            # here we wait up to 15 seconds until the webdriver manages to find the Expected Condition of
            # the element with the class name of "success-lead__action" to be clickable
            element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "success-lead__action")))
            print("successfully enrolled!")

            # update db
            checkout_tr.remarks = "enrolled"
            session.commit()
            print("row", str(checkout_tr.id), "updated\n")


        # what happens if you have already enrolled in the course?
        # Udemy will redirect you to the overview page for that course instead.
        # the URL will look something like this 'udemy.com/the-course-i-already-enrolled-in/v1/overview'
        # we simply check if the url ends with overview. if so, we update our db that it is already enrolled.
        elif driver.current_url.endswith("/overview"):
            print("already enrolled. skipping to next...")

            # update db
            checkout_tr.remarks = "enrolled"
            session.commit()
            print("row", str(checkout_tr.id), "updated\n")

        # what if Udemy rediects you to a mysterious place?
        # let's just ignore it (warning: not a good practice, you should probably log this so that you will
        # know how to deal with such redirects in the future. but the chances here are slim so we ignore it.)
        else:
            print("an error has occured. skipping to next...")

    # Author's Remarks: you can remove "filter(Course.remarks.isnot("enrolled"))" to re-check all courses which are free.

    # finally, we quit the webdriver
    driver.close()
    print("all reddit enrollment completed.\n")
