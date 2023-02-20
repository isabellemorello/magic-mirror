import datetime as dt
import  locale

import json

# locale.setlocale(locale.LC_ALL, 'it_IT')

class Calendar:
    def __init__(self, calendar):
        self.calendar = calendar
        self.name = self.get_name()
        self.date = self.get_date()
        self.date_number = self.get_date_number()
        self.weekday = self.get_date_weekday()
        self.month = self.get_date_month()
        self.hour = self.get_hour()


    def get_name(self):
        # with open(self.calendar, "r") as data_file:
        #     event_names = json.load(data_file)
        event_names = self.calendar
        event_name = [ev[1] for ev in event_names]
        # print(event_name)
        return event_name


    def get_date(self):
        date = []
        # with open(self.calendar, "r") as data_file:
        #     event_names = json.load(data_file)
        event_names = self.calendar
        event_date = [ev[0] for ev in event_names]
        # print(event_date)

        for d in event_date:
            dateTime = str(d[0:10]).split("-")
            date.append(dt.date(day=int(dateTime[2]), month=int(dateTime[1]), year=int(dateTime[0])))
        # print(date)
        return date

    def get_date_number(self):
        number_list = []
        date = self.get_date()
        for d in date:
            number_list.append(d.day)
        # print(number_list)
        return number_list


    def get_date_weekday(self):
        weekday_list = []
        date = self.get_date()
        for wd in date:
            weekday_list.append(wd.strftime("%A"))
        # print(weekday_list)
        return weekday_list


    def get_date_month(self):
        month_list = []
        date = self.get_date()
        for m in date:
            month_list.append(m.strftime("%m"))
        # print(month_list)
        return month_list


    def get_hour(self):
        hours = []
        # with open(self.calendar, "r") as data_file:
        #     event_names = json.load(data_file)
        event_names = self.calendar
        hour_list = [ev[0] for ev in event_names]
        # print(hour_list)

        for h in hour_list:
            try:
                time = str(h[11:19]).split(":")
                hours.append(dt.time(hour=int(time[0]), minute=int(time[1]), second=int(time[2])).strftime("%H:%M"))
            except ValueError:
                hours.append("Tutto il giorno")
        # print(hours)
        return hours


# c = Calendar("../static/calendar_events.json")
# c.get_hour()
# for i in range(0,5):
#     i += 1
#     print(f"Hai un evento: {c.name[i]}, {c.weekday[i]} {c.date_number[i]}/{c.month[i]} alle ore {c.hour[i]}")