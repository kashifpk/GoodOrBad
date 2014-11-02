# -*- coding: utf-8 -*-
import kivy
kivy.require('1.8.0')

from kivy.app import App

from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

#import plyer


class MainWindow(BoxLayout):
    "Main screen of the app"

    def do_action(self, action):
        "Called for good or bad button presses"
        self.set_status(action)
        #plyer.notification.notify("Good or Bad?", "Action is " + str(action))
        #self.set_status(plyer.uniqueid.id)

    def set_status(self, msg):
        self.lbl_status.text = msg


class GoodOrBadApp(App):
    "The main app"

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    GoodOrBadApp().run()