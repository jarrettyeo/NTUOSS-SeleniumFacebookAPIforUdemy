import bitly_api
# https://github.com/bitly/bitly-api-python/issues/39
# https://www.dropbox.com/s/7vbsda9hbgodq77/bitly.zip?dl=0
# must include both extra files into working dir first

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

# import os

engine = create_engine('sqlite:///courses.db')
Session = sessionmaker(bind=engine)
session = Session()

BITLY_ACCESS_TOKEN = "REPLACE_ME" # replace this with your access key, for example: BITLY_ACCESS_TOKEN = "894c3beijr893nrd398"

bitly = bitly_api.Connection(access_token=BITLY_ACCESS_TOKEN)

for bitly_tr in session.query(Course).filter(Course.status == "bit.ly url found"):
    bitly_hash = bitly_tr.bitly_url.split("http://bit.ly/")[1]
    data = bitly.expand(hash=bitly_hash)

    try:
        print(data[0]['long_url'])
        bitly_tr.expanded_url = data[0]['long_url']
        bitly_tr.status = "expanded url found"
        session.commit()
        print("row", str(bitly_tr.id), "updated\n")

    except:
        print("error, skipping to next...\n")
        pass
