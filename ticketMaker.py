from datetime import datetime as dt
import json

class TicketMaker:
    def __init__(self, number=None, sid=None, sector=None, dict=None):
        if dict != None:
            if type(dict) == type(str):
                dict = json.loads(dict)
            self.number = dict['number']
            self.sid = dict['sid']
            self.sector = dict['sector']
            self.year = dict['year']
            self.month = dict['month']
            self.day = dict['day']
            self.hour = dict['hour']
            self.minute = dict['minute']
            self.second = dict['second'] 
        else:
            self.number = number
            self.sid = sid
            self.sector = sector
            self.year = dt.now().year
            self.month = dt.now().month
            self.day = dt.now().day
            self.hour = dt.now().hour
            self.minute = dt.now().minute
            self.second = dt.now().second


    #dunder methods
    #>
    def __gt__(self, other):
        if self.year > other.year:
            return True
        elif self.month > other.month:
            return True
        elif self.day > other.day:
            return True
        elif self.hour > other.hour:
            return True
        elif self.minute > other.minute:
            return True
        elif self.second > other.second:
            return True
        

    #>=
    def __ge__(self, other):
        pass

    #<
    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.month < other.month:
            return True
        elif self.day < other.day:
            return True
        elif self.hour < other.hour:
            return True
        elif self.minute < other.minute:
            return True
        elif self.second < other.second:
            return True

    #<=
    def __le__(self, other):
        pass

    #==
    def __eq__(self, other):
        pass

    #!=
    def __ne__(self, other):
        pass

    def dict(self):
        return {
            'number':self.number, 
            'sid':self.sid,
            'year':self.year,
            'month':self.month,
            'day':self.day,
            'hour':self.hour,
            'minute':self.minute,
            'second':self.second
        }

    def strdict(self):
        return json.dumps(self.dict())

    def __str__(self):
        return self.number