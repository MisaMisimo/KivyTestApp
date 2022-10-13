'''
Application example using build() + return
==========================================

An application can be built if you return a widget on build(), or if you set
self.root.
'''

import kivy
import kivymd
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.label import Label


class TestApp(App):

    def build(self):
        # return a Button() as a root widget
        return Label(text='Test App Succesful!')


if __name__ == '__main__':
    TestApp().run()