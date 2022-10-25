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
from kivy.clock import Clock
from kivy.properties import BooleanProperty
import timeit

__author__ = "Mark Rauch Richards"

DOUBLE_TAP_TIME = 0.2   # Change time in seconds
LONG_PRESSED_TIME = 0.3  # Change time in seconds


class SelectableListItem(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
   index = None
   selected = BooleanProperty(False)
   selectable = BooleanProperty(True)
   def __init__(self, **kwargs):
      super(SelectableListItem, self).__init__(**kwargs)
      self.start = 0
      self.single_hit = 0
      self.press_state = False
      self.register_event_type('on_single_press')
      self.register_event_type('on_double_press')
      self.register_event_type('on_long_press')
   def refresh_view_attrs(self, rv, index, data):
      ''' Catch and handle the view changes '''
      self.index = index
      return super(SelectableListItem, self).refresh_view_attrs(
         rv, index, data)
   def on_touch_down(self, touch):
      if self.collide_point(touch.x, touch.y):
         self.start = timeit.default_timer()
         if touch.is_double_tap:
               self.press_state = True
               self.single_hit.cancel()
               self.dispatch('on_double_press')
      else:
         return super(SelectableListItem, self).on_touch_down(touch)

   def on_touch_up(self, touch):
      if self.press_state is False:
         if self.collide_point(touch.x, touch.y):
               stop = timeit.default_timer()
               awaited = stop - self.start

               def not_double(time):
                  nonlocal awaited
                  if awaited > LONG_PRESSED_TIME:
                     self.dispatch('on_long_press')
                  else:
                     self.dispatch('on_single_press')

               self.single_hit = Clock.schedule_once(not_double, DOUBLE_TAP_TIME)
         else:
               return super(SelectableListItem, self).on_touch_down(touch)
      else:
         self.press_state = False
   def on_touch_down(self, touch):
      ''' Add selection on touch down '''
      if super(SelectableListItem, self).on_touch_down(touch):
         return True
      if self.collide_point(*touch.pos) and self.selectable:
         return self.parent.select_with_touch(self.index, touch)
   def apply_selection(self, rv, index, is_selected):
      ''' Respond to the selection of items in the view. '''
      self.selected = is_selected
      if is_selected:
         print("selection changed to {0}".format(rv.data[index]))
      else:
         print("selection removed for {0}".format(rv.data[index]))
   def on_single_press(self):
      print("single press")
      print("index", self.index)

   def on_double_press(self):
      print("double press")
      print("index", self.index)

   def on_long_press(self):
      print("long press")
      print("index", self.index)