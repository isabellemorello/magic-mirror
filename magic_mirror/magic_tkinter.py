import time
from tkinter import *
import customtkinter
import datetime as dt
import locale
from random import randint
import google_calendar.calendar_google as gc
import microsoft_to_do_list.to_do_list as to_do
import microsoft_to_do_list.ms_graph_token as graph_token
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


# def app():
def app(microsoft_task_routine, microsoft_task_ricorda):
# def app(calendar, microsoft_task_routine, microsoft_task_ricorda):
    # --------------------------------------------- VARIABLES ----------------------------------------------------
    now = dt.datetime.now()
    clock = now.strftime("%H:%M:%S")
    date = now.strftime("%A, %d %B")
    # get_calendar = calendar
    # calendar_m = Calendar(get_calendar)
    calendar_m = Calendar("static/calendar_events.json")

    get_routine = microsoft_task_routine
    get_ricorda = microsoft_task_ricorda

    # get_routine = to_do.get_method(secrets_path="secrets.json", activities_path="static/activities.json", path="static/routine_task.json", task="ID_ROUTINE_TASK")
    # get_ricorda = to_do.get_method(secrets_path="secrets.json", activities_path="static/activities.json", path="static/ricorda_di_task.json", task="ID_RICORDA_DI_TASK")

    routine_list = ToDoList(get_routine).task
    ricorda_di_list = ToDoList(get_ricorda).task

    # routine_list = ToDoList("static/routine_task.json").task
    # ricorda_di_list = ToDoList("static/ricorda_di_task.json").task

    weather_data = "static/weather_one_call.json"
    # weather_data = open_weather_data
    weather = Weather(weather_data)
    icon = weather.icon
    daily_icons = weather.daily_icon
    daily_max_min = weather.daily_max_min
    weekday_count = 0
    weekday = ""
    # room_temperature = 16
    room_temperature = Temperature("static/temperature.json").temperature
    is_me = True


    # ------------------------------------------ Tkinter WINDOW -------------------------------------------------
    window = Tk()
    window.title("Isabelle's Magic Mirror")
    window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
    # window.geometry("1400x750")
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


    def refresh():
        # calendar_ev, microsoft_task_routine, microsoft_task_ricorda, open_weather_map = api_request()
        microsoft_task_routine, microsoft_task_ricorda, open_weather_map = api_request()
        window.destroy()
        app(microsoft_task_routine, microsoft_task_ricorda)
        # app(calendar_ev, microsoft_task_routine, microsoft_task_ricorda)

    def weather_icon_f():
        image_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        u = urlopen(image_url)
        raw_data = u.read()
        u.close()
        return raw_data


    def change_style(value, label):
        if value == "notStarted":
            label.configure(text_color="white", font=font_normal)
        elif value == "completed":
            label.configure(text_color="pink", font=font_done)


    def change_check_status(checkbtn, var, key, list, id_task):
        if var.get() == "completed":
            list[key][1] = var.get()
            checkbtn.configure(font=font_done, fg_color="pink", text_color="pink")
        else:
            list[key][1] = var.get()
            checkbtn.configure(font=font_normal, fg_color="white", text_color="white")
        print(f"Clicked: {var.get()}")
        print(list.values())
        to_do.patch_method(generate_access_token=graph_token.generate_access_token("microsoft_to_do_list/api_token_access.json", "secrets.json"), title=key, status_value=list[key][1], secrets_path="secrets.json", task=list, task_list=id_task)


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

    if is_me:
        greet_label = Label(frame2, text="Ciao Isabelle Michelle! ☻", fg="white", bg="black", font=("Arial", 26, "bold"), anchor="center")
    else:
        greet_label = Label(frame2, text="Benvenuto. Sono il Magic Mirror di Isabelle!", wraplength=400, fg="white", bg="black", font=("Arial", 26, "bold"), anchor="center")
    greet_label.grid(row=2, column=0, padx=50, pady=20)

    quote_text_label = Label(frame2, text="", wraplength=500, fg="white", bg="black", justify="center", font=("Arial", 20, "normal"), width=50)
    quote_author_label = Label(frame2, text="", fg="white", bg="black", justify="center", font=("Arial", 15, "normal"), width=50)
    quote_text_label.grid(row=3, column=0, padx=50, sticky="wesn")
    quote_author_label.grid(row=4, column=0, padx=50, sticky="wesn")


    clock_func()
    window.after(8000, destroy_greet)
    quote_text_label.after(8025, change_quote)

    refresh_button  = customtkinter.CTkButton(frame2, text="♻︎ Refresh", compound="left", corner_radius=8, command=refresh, fg_color="pink", text_color="black", font=("Arial", 24, "bold"))
    refresh_button.grid(row=5, column=0, sticky="s", pady=(window.winfo_screenheight()-525,0), ipady=10, ipadx=30)


    # -------------------------------------------------- Calendario ---------------------------------------------------
    calendar_title_label = Label(frame4, text="Calendario:", fg="white", bg="black", font=("Arial", 15, "bold"))
    calendar_title_label.grid(row=0, column=0, pady=(0, 5), sticky="w")

    if is_me:
        for counter in range(0, 4):
            frame_c = Frame(frame4, background="black")
            frame_c.grid(row=1 + counter, column=0, sticky="w", pady=(0, 20), padx=(0, 5))

            frame_c1 = Frame(frame4, background="black")
            frame_c1.grid(row=1 + counter, column=1, sticky="w", pady=(0, 5), padx=(20, 0))

            number_c = Label(frame_c, text=calendar_m.date_number[counter], fg="white", bg="black", font=("Arial", 20))
            number_c.grid(row=0, column=0, sticky="nw")
            day_c = Label(frame_c, text=f" / {calendar_m.month[counter]}  {calendar_m.weekday[counter]}", fg="white", bg="black", font=("Arial", 15))
            day_c.grid(row=0, column=1, sticky="nw")
            hour_c = Label(frame_c, text=calendar_m.hour[counter], fg="white", bg="black", font=("Arial", 15), anchor="w")
            hour_c.grid(row=1, column=1, sticky="wesn", columnspan=2)
            name_c = Label(frame_c1, text=calendar_m.name[counter], fg="white", bg="black", wraplength=200, font=("Arial", 15), anchor="w")
            name_c.grid(row=1, column=0, sticky="wesn", rowspan=2)
    else:
        not_allowed_calendar = Label(frame4, text="☠ Non puoi vedere questa sezione perché non ti conosco! ☹︎", wraplength=400,
                                    fg="white", bg="black", font=("Arial", 15, "normal"))
        not_allowed_calendar.grid(row=1, column=0, pady=(30, 150))


    # -------------------------------------------------- To Do List ---------------------------------------------------
    font_normal = ("Arial", 20, "normal")
    font_done = ("Arial", 20, "overstrike")
    my_ref = {}

    #ROUTINE
    routine_title_label = Label(frame5, text="Routine:", fg="white", bg="black", font=("Arial", 15, "bold"))
    routine_title_label.grid(row=0, column=0, pady=(30, 5), sticky="w")

    counter = 0
    if is_me:
        for key, v in routine_list.items():
            value = v[1]
            is_routine_checked = StringVar()
            is_routine_checked.set(value)
            routine_label = customtkinter.CTkCheckBox(frame5, variable=is_routine_checked, onvalue="completed",
                                                      offvalue="notStarted", command=lambda k=key: change_check_status(
                    var=my_ref[k][1], checkbtn=my_ref[k][0], key=k, list=routine_list, id_task="ID_ROUTINE_TASK"), text=f"︎   {key}", fg_color="white",
                                                      text_color="white", bg_color="black", font=font_normal)
            change_style(is_routine_checked.get(), routine_label)
            counter += 1
            routine_label.grid(row=1 + counter, column=0, sticky="w", pady=5)
            my_ref[key] = [routine_label, is_routine_checked]
    else:
        not_allowed_routine = Label(frame5, text="☠ Non puoi vedere questa sezione perché non ti conosco! ☹︎", wraplength=400, fg="white", bg="black", font=("Arial", 15, "normal"))
        not_allowed_routine.grid(row=1, column=0, pady=(30,100))


    # RICORDA DI
    ricorda_title_label = Label(frame6, text="Ricorda di:", fg="white", bg="black", font=("Arial", 15, "bold"))
    ricorda_title_label.grid(row=0, column=0, pady=(30, 5), sticky="w")

    counter2 = 0
    if is_me:
        for key, v in ricorda_di_list.items():
            value = v[1]
            is_ricorda_di_checked = StringVar()
            is_ricorda_di_checked.set(value)
            ricorda_di_label = customtkinter.CTkCheckBox(frame6, variable=is_ricorda_di_checked, onvalue="completed",
                                                      offvalue="notStarted", command=lambda k=key: change_check_status(
                    var=my_ref[k][1], checkbtn=my_ref[k][0], key=k, list=ricorda_di_list, id_task="ID_RICORDA_DI_TASK"), text=f"︎   {key}", fg_color="white",
                                                      text_color="white", bg_color="black", font=font_normal)
            change_style(is_ricorda_di_checked.get(), ricorda_di_label)
            counter2 += 1
            ricorda_di_label.grid(row=1 + counter2, column=0, sticky="w", pady=5)
            my_ref[key] = [ricorda_di_label, is_ricorda_di_checked]
    else:
        not_allowed_ricorda = Label(frame6, text="☠ Non puoi vedere questa sezione perché non ti conosco! ☹︎", wraplength=400, fg="white", anchor="w",
                                bg="black", font=("Arial", 15, "normal"))
        not_allowed_ricorda.grid(row=1, column=0, pady=(30,0))


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


def api_request():
    # calendar_ev = gc.main("static/calendar_events.json", "google_calendar/credentials.json")
    microsoft_task_routine = to_do.get_method(
        generate_access_token=graph_token.generate_access_token("microsoft_to_do_list/api_token_access.json",
                                                                "secrets.json"), secrets_path="secrets.json",
        activities_path="static/activities.json", path="static/routine_task.json", task="ID_ROUTINE_TASK")
    microsoft_task_ricorda = to_do.get_method(
        generate_access_token=graph_token.generate_access_token("microsoft_to_do_list/api_token_access.json",
                                                                "secrets.json"), secrets_path="secrets.json",
        activities_path="static/activities.json", path="static/ricorda_di_task.json", task="ID_RICORDA_DI_TASK")
    open_weather_map = open_weather.app_weather("static/weather_one_call.json", "secrets.json")
    return  microsoft_task_routine, microsoft_task_ricorda, open_weather_map
    # return calendar_ev, microsoft_task_routine, microsoft_task_ricorda, open_weather_map


if __name__ == "__main__":
    try:
        temperature = read_temp("static/temperature.json")
        while temperature == None:
            temperature = read_temp("static/temperature.json")
        # calendar_ev, microsoft_task_routine, microsoft_task_ricorda, open_weather_map = api_request()
        microsoft_task_routine, microsoft_task_ricorda, open_weather_map = api_request()
        # calendar_ev = gc.main("static/calendar_events.json", "google_calendar/credentials.json")
        # microsoft_task_routine = to_do.get_method(generate_access_token=graph_token.generate_access_token("microsoft_to_do_list/api_token_access.json", "secrets.json"), secrets_path="secrets.json", activities_path="static/activities.json", path="static/routine_task.json", task="ID_ROUTINE_TASK")
        # microsoft_task_ricorda = to_do.get_method(generate_access_token=graph_token.generate_access_token("microsoft_to_do_list/api_token_access.json", "secrets.json"), secrets_path="secrets.json", activities_path="static/activities.json", path="static/ricorda_di_task.json", task="ID_RICORDA_DI_TASK")
        # open_weather_map = open_weather.app_weather("static/weather_one_call.json", "secrets.json")

    except Exception as e:
        print(e)
    else:
        # app()
        app(microsoft_task_routine, microsoft_task_ricorda)
        # app(calendar_ev, microsoft_task_routine, microsoft_task_ricorda)

    # temperature = read_temp("static/temperature.json")
    # while temperature == None:
    #     temperature = read_temp("static/temperature.json")
    # open_weather_map = open_weather.app_weather("static/weather_one_call.json")
    app()
