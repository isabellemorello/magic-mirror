from tkinter import *
import datetime as dt
import locale
from random import randint
import google_calendar.calendar_google as gc
import microsoft_to_do_list.to_do_list as to_do
# import microsoft_to_do_list.ms_graph_token as graph_token
import open_weather_map.open_weather_map as open_weather
import static.quotes as quotes
from models.calendar_model import Calendar
from models.to_do_list_model import ToDoList
from models.weather_model import Weather
from models.temperature_model import Temperature
from urllib.request import urlopen
from sensor_read import read as read_temp
import os

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

locale.setlocale(locale.LC_ALL, 'it_IT')


def app():
    # --------------------------------------------- VARIABLES ----------------------------------------------------
    now = dt.datetime.now()
    clock = now.strftime("%H:%M:%S")
    date = now.strftime("%A, %d %B")
    # size = 14
    calendar_m = Calendar("static/calendar_events.json")
    routine_list = ToDoList("static/routine_task.json").title_list
    ricorda_di_list = ToDoList("static/ricorda_di_task.json").title_list
    weather_data = "static/weather_one_call.json"

    weather = Weather(weather_data)
    icon = weather.icon
    daily_icons = weather.daily_icon
    daily_max_min = weather.daily_max_min
    weekday_count = 0
    weekday = ""
    # room_temperature = 16
    room_temperature = Temperature("static/temperature.json").get_temperature()
    print(f"La temperatura della stanza è: {room_temperature}")

    # ------------------------------------------ Tkinter WINDOW -------------------------------------------------
    window = Tk()
    window.title("Isabelle's Magic Mirror")
    window.geometry("1400x750")
    window.config(bg="black", padx=25, pady=25)

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)


    # -------------------------------------------- FUNCTIONS -------------------------------------------------
    def clock_func():
        """Display a digital clock"""
        clock = dt.datetime.now().strftime("%H:%M:%S")
        date = dt.datetime.now().strftime("%A, %d %B")
        clock_label.config(text=clock)
        date_label.config(text=date)
        clock_label.after(1000, clock_func)


    def change_quote():
        """Choose a random motivational quote"""
        quote = quotes.quotes[randint(1, len(quotes.quotes) - 1)]
        q_text = quote["text"]
        q_author = quote["author"]
        quote_text_label.config(text=q_text)
        quote_author_label.config(text=q_author)


    def destroy_greet():
        """Destroy greet label"""
        greet_label.destroy()


    def weather_icon_f():
        image_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        u = urlopen(image_url)
        raw_data = u.read()
        u.close()
        return raw_data


    # ----------------------------------------------------------------------------------------------------------
    # -------------------------------------------------- GUI ---------------------------------------------------
    frame1 = Frame(window, background="black")
    frame1.grid(row=0, column=0, sticky="wesn", padx=5)
    frame2 = Frame(window, background="black")
    frame2.grid(row=0, column=1, sticky="wesn", padx=5)
    frame3 = Frame(window, background="black")
    frame3.grid(row=0, column=2, sticky="wesn", padx=5)
    frame4 = Frame(frame1, background="black")
    frame4.grid(row=1, column=0, sticky="wesn")
    frame5 = Frame(frame1, background="black")
    frame5.grid(row=2, column=0, sticky="wesn")
    frame6 = Frame(frame1, background="black")
    frame6.grid(row=3, column=0, sticky="wesn")

    clock_label = Label(frame2, text=clock, fg="white", bg="black", font=("Arial", 40, "bold"))
    clock_label.grid(row=0, column=0, sticky="wesn")
    date_label = Label(frame2, text=date, fg="white", bg="black", font=("Arial", 20, "normal"))
    date_label.grid(row=1, column=0, padx=20, sticky="wesn", pady=(0, 60))

    greet_label = Label(frame2, text="Ciao Isabelle Michelle", fg="white", bg="black", font=("Arial", 20, "normal"), anchor="center", width=50)
    greet_label.grid(row=2, column=0, padx=50, pady=20)

    quote_text_label = Label(frame2, text="", wraplength=500, fg="white", bg="black", justify="center", font=("Arial", 20, "normal"), width=50)
    quote_author_label = Label(frame2, text="", fg="white", bg="black", justify="center", font=("Arial", 15, "normal"), width=50)
    quote_text_label.grid(row=3, column=0, padx=50, sticky="wesn")
    quote_author_label.grid(row=4, column=0, padx=50, sticky="wesn")


    clock_func()
    window.after(4000, destroy_greet)
    quote_text_label.after(4025, change_quote)


    # -------------------------------------------------- Calendario ---------------------------------------------------
    calendar_title_label = Label(frame4, text="Calendario:", fg="white", bg="black", font=("Arial", 15, "bold"))
    calendar_title_label.grid(row=0, column=0, pady=(0, 5), sticky="w")

    for i in range(0, 4):
        frame_c = Frame(frame4, background="black")
        frame_c.grid(row=1 + i, column=0, sticky="w", pady=(0, 20), padx=(0, 5))

        frame_c1 = Frame(frame4, background="black")
        frame_c1.grid(row=1 + i, column=1, sticky="w", pady=(0, 5), padx=(20, 0))

        number_c = Label(frame_c, text=calendar_m.date_number[i], fg="white", bg="black", font=("Arial", 20))
        number_c.grid(row=0, column=0, sticky="nw")
        day_c = Label(frame_c, text=f" / {calendar_m.month[i]}  {calendar_m.weekday[i]}", fg="white", bg="black", font=("Arial", 15))
        day_c.grid(row=0, column=1, sticky="nw")
        hour_c = Label(frame_c, text=calendar_m.hour[i], fg="white", bg="black", font=("Arial", 15), anchor="w")
        hour_c.grid(row=1, column=1, sticky="wesn", columnspan=2)
        name_c = Label(frame_c1, text=calendar_m.name[i], fg="white", bg="black", wraplength=200, font=("Arial", 15), anchor="w")
        name_c.grid(row=1, column=0, sticky="wesn", rowspan=2)


    # -------------------------------------------------- To Do List ---------------------------------------------------
    routine_title_label = Label(frame5, text="Routine:", fg="white", bg="black", font=("Arial", 15, "bold"))
    routine_title_label.grid(row=0, column=0, pady=(30, 5), sticky="w")

    for i in range(len(routine_list)):
        routine_label = Label(frame5, text=f"☐   {routine_list[i]}", fg="white", bg="black", font=("Arial", 15))
        i += 1
        routine_label.grid(row=1+i, column=0, sticky="w")

    ricorda_title_label = Label(frame6, text="Ricorda di:", fg="white", bg="black", font=("Arial", 15, "bold"))
    ricorda_title_label.grid(row=0, column=0, pady=(30, 5), sticky="w")

    for i in range(len(ricorda_di_list)):
        ricorda_di_label = Label(frame6, text=f"☐   {ricorda_di_list[i]}", fg="white", bg="black", font=("Arial", 15))
        i += 1
        ricorda_di_label.grid(row=1+i, column=0, sticky="w")


    # -------------------------------------------------- Meteo ---------------------------------------------------
    raw_data = weather_icon_f()

    today_label = Label(frame3, text="OGGI", fg="white", bg="black", font=("Arial", 20, "normal"))
    today_label.grid(row=0, column=0, sticky="w")

    icon_image = PhotoImage(data=raw_data)
    icon_label = Label(frame3, image=icon_image, bg="black")
    icon_label.image = icon_image
    icon_label.grid(row=0, column=1, sticky="e")

    weather_temp = Label(frame3, text=f"{weather.temperature}°", fg="white", bg="black", font=("Arial", 30, "normal"))
    weather_temp.grid(row=0, column=2, sticky="e")

    alert_room_temperature_label = Label(frame3, text="⚠️🥶", fg="white", bg="black", font=("Arial", 20, "normal"))

    if room_temperature <= 17 and room_temperature != None:
        alert_room_temperature_label.grid(row=1, column=1, sticky=E)
    else:
        alert_room_temperature_label.grid_forget()


    room_temperature_label = Label(frame3, text=f"{room_temperature}°", fg="white", bg="black", font=("Arial", 20, "normal"))
    room_temperature_label.grid(row=1, column=2, sticky=E)

    room_temperature_text_label = Label(frame3, text="Temperatura stanza", fg="white", bg="black", font=("Arial", 14, "normal"))
    room_temperature_text_label.grid(row=2, column=0, sticky="e", columnspan=3, pady=(0, 20))

    for n in range(0, 4):
        weekday_count += 1
        date = dt.date.today()
        try:
            weekday = dt.date(year=date.year, month=date.month, day=date.day + weekday_count).strftime("%d %a").upper()
        except ValueError:
            if date.month == 4 or date.month == 6 or date.month == 9 or date.month == 11:
                weekday = dt.date(year=date.year, month=date.month + 1, day=date.day + weekday_count - 30).strftime("%d %a").upper()
            elif date.month == 2:
                if date.year % 4 == 0:
                    if date.year % 100 == 0:
                        if date.year % 400 == 0:
                            weekday = dt.date(year=date.year, month=date.month + 1, day=date.day + weekday_count - 29).strftime("%d %a").upper()
                        else:
                            weekday = dt.date(year=date.year, month=date.month + 1, day=date.day + weekday_count - 28).strftime("%d %a").upper()
                    else:
                        weekday = dt.date(year=date.year, month=date.month + 1, day=date.day + weekday_count - 29).strftime("%d %a").upper()
                else:
                    weekday = dt.date(year=date.year, month=date.month + 1, day=date.day + weekday_count - 28).strftime("%d %a").upper()
            else:
                weekday = dt.date(year=date.year, month=date.month + 1, day=date.day + weekday_count - 31).strftime("%d %a").upper()


        frame = Frame(frame3, background="black")
        frame.grid(row=3+n, column=0, sticky="wesn", pady=10, columnspan=2)

        frame1 = Frame(frame3, background="black")
        frame1.grid(row=3+n, column=2,  pady=10)

        image_url = f"http://openweathermap.org/img/wn/{daily_icons[n]}@2x.png"
        u = urlopen(image_url)
        raw_data = u.read()
        u.close()

        icon_image = PhotoImage(data=raw_data)
        icon_label = Label(frame, image=f"{icon_image}", bg="black")
        icon_label.image = icon_image
        icon_label.grid(row=0, column=1, sticky=E, rowspan=2)

        max_temp_label = Label(frame1, text=f"max: {daily_max_min[n][0]}", fg="white", bg="black", font=("Arial", 16, "normal"))
        max_temp_label.grid(row=0, column=2, sticky="nwes")

        min_temp_label = Label(frame1, text=f"min: {daily_max_min[n][1]}", fg="white", bg="black", font=("Arial", 16, "normal"))
        min_temp_label.grid(row=1, column=2, sticky="swen")

        day_label = Label(frame, text=weekday, fg="white", bg="black", font=("Arial", 16, "normal"))
        day_label.grid(row=0, column=0, sticky=W, rowspan=2)


    window.mainloop()

if __name__ == "__main__":
    try:
        temperature = read_temp("static/temperature.json")
        while temperature == None:
            temperature = read_temp("static/temperature.json")
        # calendar_ev = gc.main("static/calendar_events.json", "google_calendar/credentials.json")
        microsoft_task = to_do.app_to_do(activities_path="static/activities.json", routine_path="static/routine_task.json", ricorda_path="static/ricorda_di_task.json")
        # microsoft_task = to_do.app_to_do(generate_access_token=graph_token.generate_access_token("microsoft_to_do_list/api_token_access.json"), activities_path="static/activities.json", routine_path="static/routine_task.json", ricorda_path="static/ricorda_di_task.json")
        open_weather_map = open_weather.app_weather("static/weather_one_call.json")
    except Exception as e:
        print(e)
    else:
        app()
    # temperature = read_temp("static/temperature.json")
    # while temperature == None:
    #     temperature = read_temp("static/temperature.json")
    # open_weather_map = open_weather.app_weather("static/weather_one_call.json")
    # app()
