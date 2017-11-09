import requests, urllib # , beautifulsoup4
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

# Initialise Database
engine = create_engine('sqlite:///courses.db')
Session = sessionmaker(bind=engine)
session = Session()

# result = requests.get("http://freecoupondiscount.com/udemy-coupon-how-to-communicate-with-more-influence-impact/")
# assert result.status_code != "200"
#
# c = result.content
# soup = BeautifulSoup(c, "html.parser")
# samples = soup.find_all("a", "btn_offer_block re_track_btn medium")
# print(urllib.parse.unquote(samples[0].attrs['href'].split('murl=')[1]))

for expanded_tr in session.query(Course).filter(Course.status == "expanded url found"):
    result = requests.get(expanded_tr.expanded_url)
    assert result.status_code != "200"

    try:
        soup = BeautifulSoup(result.content, "html.parser")
        sample = soup.find("a", "btn_offer_block re_track_btn medium")
        untrimmed_url = sample.attrs['href']

        if "murl=" in untrimmed_url:
            udemy_url = urllib.parse.unquote(untrimmed_url.split('murl=')[1])
        elif "RD_PARM1=" in untrimmed_url:
            udemy_url = urllib.parse.unquote(untrimmed_url.split('RD_PARM1=')[1])
        elif untrimmed_url.startswith("https://www.udemy.com/"):
            udemy_url = udemy_url
        print(udemy_url)

        expanded_tr.udemy_url = udemy_url
        expanded_tr.status = "udemy url found"
        session.commit()
        # wait = input("PRESS ENTER TO CONTINUE.")
        print("row", str(expanded_tr.id), "updated\n")

    except:
        print("error on row", str(expanded_tr.id),"skipping to next...\n")
        pass
