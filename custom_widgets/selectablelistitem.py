#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   MultiExpressionButton extends the Kivy Button object and adds three different events; on_single_press,
   on_double_press, and on_double_press. DOUBLE_PRESS_TIME determines how long it will wait for the second press before
   concluding it is a single press and LONG_PRESS_TIME determines how long the button must be held down to be considered
   a long press.
"""
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.properties import BooleanProperty
import timeit

__author__ = "Mark Rauch Richards"

LONG_PRESSED_TIME = 0.6  # Change time in seconds

class EditTransactionDialog(MDBoxLayout):
   pass
class SelectableListItem(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
   index = None
   long_press_threshold_reached = False
   long_press_event = None
   def __init__(self, **kwargs):
      super(SelectableListItem, self).__init__(**kwargs)
   def refresh_view_attrs(self, rv, index, data):
      ''' Catch and handle the view changes '''
      self.index = index
      return super(SelectableListItem, self).refresh_view_attrs(
         rv, index, data)
   def _do_long_press(self, *kwargs):
      if (self.continuous_press):
         self.on_long_press()
   def on_press(self, *kwargs):
      self.continuous_press = True
      self.long_press_event = Clock.schedule_once(self._do_long_press, LONG_PRESSED_TIME)
   def on_release(self, *kwargs):
      if(self.continuous_press):
         Clock.unschedule(self.long_press_event)
   def on_long_press(self, *kwargs):
      print("Long press on index " + str(self.index))
