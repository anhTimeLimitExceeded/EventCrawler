from datetime import date, datetime, timedelta
import re

class DataHolder:
    def __init__(self):
        self.free_foods = []
        self.hackathons = []
    
    def getFreeFoods(self, limit):
        s = ""
        for i in range (min(limit, len(self.free_foods))):
            s += str(i+1) + ". " + self.free_foods[i].__str__() + "\n"

        return s
    
    def getEventsToString(self, events):
        s = ""
        cnt = 1
        for event in events:
            s += str(cnt) + ". " + event.__str__() + "\n"
            cnt += 1
        return s

    def getTodayFreeFood(self):
        today_events = []
        for freeFoodEvent in self.free_foods:
            if (freeFoodEvent.startsOn.date() <= datetime.today().date() and freeFoodEvent.endsOn.date() >= datetime.today().date()):
                today_events.append(freeFoodEvent)

        return self.getEventsToString(today_events)

    def getTomorrowFreeFood(self):
        today_events = []
        for freeFoodEvent in self.free_foods:
            if (freeFoodEvent.startsOn.date() <= (datetime.today() + timedelta(days=1)).date() and freeFoodEvent.endsOn.date() >= (datetime.today() + timedelta(days=1)).date()):
                today_events.append(freeFoodEvent)

        return self.getEventsToString(today_events)