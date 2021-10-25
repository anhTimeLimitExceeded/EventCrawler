import requests
import calendar
from datetime import date, datetime, timedelta
import logging
import logging.handlers
from dataholder import DataHolder
import email_bot
import schedule
import time

logging.basicConfig(handlers=[logging.FileHandler(filename="main.log", 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('crawler')

class FreeFoodEvent: 
    def __init__(self, name, location, startsOn, endsOn, organizationName, description, link):
        self.name = name
        self.location = location
        self.startsOn = startsOn
        self.endsOn = endsOn
        self.organizationName = organizationName
        self.description = description
        self.link = link

    def __str__(self):
        return f'{self.name} by {self.organizationName} at {self.location} [{self.startsOn.strftime("%Y-%m-%d (%A) %I:%M%p")} to {self.endsOn.strftime("%I:%M%p")}]({self.link})'

def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def crawl(dataHolder):
    logger.info("start crawling")
    EVENT_LINK = "https://depauw.campuslabs.com/engage/event/"
    today = datetime.now().strftime("%Y-%m-%d")
    res = requests.get(f'https://depauw.campuslabs.com/engage/api/discovery/event/search?endsAfter={today}T11%3A39%3A12-04%3A00&orderByField=endsOn&orderByDirection=ascending&status=Approved&take=15&benefitNames%5B0%5D=FreeFood&query=')
    blocks = res.json()['value']

    freeFoodEvents = []
    for block in blocks:
        startsOn = utc_to_local(datetime.strptime(block['startsOn'],"%Y-%m-%dT%H:%M:%S+00:00"))
        endsOn = utc_to_local(datetime.strptime(block['endsOn'],"%Y-%m-%dT%H:%M:%S+00:00"))
        freeFoodEvent = FreeFoodEvent(block['name'], block['location'], startsOn, endsOn, block['organizationName'], remove_html_tags(block['description']), EVENT_LINK+str(block['id']))
        freeFoodEvents.append(freeFoodEvent)

    dataHolder.free_foods = freeFoodEvents
    logger.info(f"finished crawling {len(freeFoodEvents)} entries")

def send_email(dataHolder):
    body = ""
    for freeFoodEvent in dataHolder.free_foods:
        if (freeFoodEvent.startsOn.date() <= datetime.today().date() and freeFoodEvent.endsOn.date() >= datetime.today().date()):
            message = f"""Name: {freeFoodEvent.name}
By: {freeFoodEvent.organizationName}
Where: {freeFoodEvent.location}
When: {freeFoodEvent.startsOn.time()} to {freeFoodEvent.endsOn.time()}
Details: {freeFoodEvent.description}
RSVP Link: {freeFoodEvent.link}
"""
            body = body + message + "\n\n"

    email_bot.send_email(freeFoodEvent.name, body)

def test():
    logger.info("looping")

def run(dataHolder):
    crawl(dataHolder)
    try:
        schedule.every().day.at("09:00").do(crawl, dataHolder=dataHolder)
        schedule.every(1).minutes.do(test)
        while True:
            schedule.run_pending()
            time.sleep(30) # wait one minute
    except Exception: 
        logging.exception("Free-food Error")