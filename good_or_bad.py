# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App

from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import mainthread

from datetime import datetime, date, timedelta
import calendar

#import plyer

from models import Deed
from db import get_db_session, setup_db

DB = get_db_session()


class MainScreen(Screen):
    "Main screen of the app"

    def do_action(self, action):
        "Called for good or bad button presses"

        db = App.get_running_app().root.db
        rec = Deed()

        if 'good' == action:
            rec.good = True

        elif 'bad' == action:
            rec.good = False

        if '' != self.txt_msg.text:
            rec.description = self.txt_msg.text

        db.add(rec)
        db.commit()
        self.set_status("Deed saved!")
        #plyer.notification.notify("Good or Bad?", "Action is " + str(action))
        #self.set_status(plyer.uniqueid.id)

    def set_status(self, msg):
        self.lbl_status.text = msg


class InfoScreen(Screen):
    pass


class MainWindow(ScreenManager):
    "Main window of the app"

    db = None

    @mainthread
    def load_info_screen_data(self):
        "This method runs in main thread and does the backend DB fetching without slowing the UI"
        today = date.today()
        info_screen = self.get_screen('info_screen')

        good_count, bad_count = Deed.get_gb_count(self.db, today)
        info_screen.lbl_gc_today.text = str(good_count)
        info_screen.lbl_bc_today.text = str(bad_count)

        end_date = today
        start_date = end_date - timedelta(days=today.weekday())
        good_count, bad_count = Deed.get_gb_count(self.db, start_date, end_date)
        info_screen.lbl_gc_week.text = str(good_count)
        info_screen.lbl_bc_week.text = str(bad_count)

        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        start_date = date(year=today.year, month=today.month, day=1)
        end_date = date(year=today.year, month=today.month, day=last_day_of_month)
        good_count, bad_count = Deed.get_gb_count(self.db, start_date, end_date)
        info_screen.lbl_gc_month.text = str(good_count)
        info_screen.lbl_bc_month.text = str(bad_count)

        start_date = date(year=today.year, month=1, day=1)
        end_date = date(year=today.year, month=12, day=31)
        good_count, bad_count = Deed.get_gb_count(self.db, start_date, end_date)
        info_screen.lbl_gc_year.text = str(good_count)
        info_screen.lbl_bc_year.text = str(bad_count)

        good_count, bad_count = Deed.get_gb_count(self.db)
        info_screen.lbl_gc_lifetime.text = str(good_count)
        info_screen.lbl_bc_lifetime.text = str(bad_count)

    def load_info_screen(self):
        "Load info screen data and then load info screen"
        self.load_info_screen_data()
        app = App.get_running_app()
        app.root.transition.direction = 'left'
        app.root.current = 'info_screen'


class GoodOrBadApp(App):
    "The main app"

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

    def build(self):
        if setup_db():
            print("Database created!")

        main_window = MainWindow()
        main_window.db = get_db_session()

        return main_window


if __name__ == '__main__':
    GoodOrBadApp().run()
