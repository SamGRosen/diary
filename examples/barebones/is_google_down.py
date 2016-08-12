from diary import Diary
import os
import time

def is_down(website, timeout=10):
    response = os.system('ping -c 1 -w {timeout} {website}'.format(
        timeout=timeout,
        website=website
    ))
    if response == 0:
        return False

    return True

# Create a logger with an output file
logger = Diary("google_status.txt")

# If a logger should point to a db give it a db
# logger = Diary("status.db")

while True:
    if is_down("google.com"):
        logger.error("GOOGLE IS DOWN!")
    else:
        logger.log("Google is up.")

    time.sleep(5)