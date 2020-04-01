from datetime import datetime, date, timedelta
import math

class TimeConverter():

    def compare_times(self, hour1 = 0, minute1 = 0, hour2 = 0, minute2=0):
        time1 = int(hour1) * 60 + int(minute1)
        time2 = int(hour2) * 60 + int(minute2)

        return time1 > time2
