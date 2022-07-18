from datetime import datetime as dt

class timewatch:
    def __init__(self, time=None):
        
        if type(time) == str:
            self.date = f"{dt.now().year:04}-{dt.now().month:02}-{dt.now().day:02}"
            self.settime(time)
        elif type(time) == type(dt.now()):
            self.date = f"{time.year:04}-{time.month:02}-{time.day:02}"
            self.hours = time.hour
            self.minutes = time.minute
            self.seconds = time.second
        elif time == None:
            self.date = f"{dt.now().year:04}-{dt.now().month:02}-{dt.now().day:02}"
            self.hours = dt.now().hour
            self.minutes = dt.now().minute
            self.seconds = dt.now().second

    def gettime(self):
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"

    def getdate(self):
        return self.date
    
    def settime(self, time:str):
        time = time.split(':')
        self.hours = int(time[0])
        self.minutes = int(time[1])
        self.seconds = int(time[2])

    def __add__(self, other):

        if self.date != other.date:
            print("addition of different dates detected")
            return -1

        seconds = self.seconds + other.seconds
        minutes = self.minutes + other.minutes
        hours = self.hours + other.hours
        if seconds >= 60:
            minutes += seconds // 60
            seconds = seconds % 60
        if minutes >= 60:
            hours += minutes // 60
            minutes = minutes % 60
        
        return timewatch(f"{hours}:{minutes:02}:{seconds:02}")

    def __sub__(self, other):

        if self.date != other.date:
            print("subtraction of diiferent dates detected")
            return -1

        seconds, minutes, hours = 0, 0, 0

        if self.seconds >= other.seconds:
            seconds = self.seconds - other.seconds
        else:
            if self.minutes != 0:
                self.minutes -= 1
                seconds = (self.seconds+60) - other.seconds
            elif self.minutes == 0:
                if self.hours == 0:
                    print("subtraction of value greater than current")
                    return -1
                self.hours -= 1
                self.minutes = 59
                seconds = (self.seconds+60) - other.seconds

        if self.minutes >= other.minutes:
            minutes = self.minutes - other.minutes
        else:
            if self.hours == 0:
                print("subtraction of value greater than current")
                return -1
            self.hours -= 1
            minutes = (self.minutes+60) - other.minutes

        if self.hours >= other.hours:
            hours = self.hours - other.hours
        else:
            print("subtraction of value greater than current")
            return -1
        
        return timewatch(f"{hours}:{minutes:02}:{seconds:02}")


    def __repr__(self):
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"

if __name__ == "__main__":
    pass
