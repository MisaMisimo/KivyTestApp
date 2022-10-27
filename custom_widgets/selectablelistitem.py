#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.properties import BooleanProperty

LONG_PRESSED_TIME = 0.6  # Change time in seconds
Builder.load_file('custom_widgets/selectablelistitem.kv')
class EditTransactionDialog(MDBoxLayout):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.orientation = "vertical"
class SelectableListItem(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
   index = None
   long_press_threshold_reached = False
   long_press_event = None
   transaction_id = None
   dialog = None
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
      print("Long press on transaction id  " + str(self.transaction_id))
      self.edit_transaction_dialog()
   def cancel_transaction_dialog(self, *kwargs):
      self.dialog.dismiss()
      self.dialog = None
   def accept_transaction_dialog(self, *kwargs):
      self.dialog.dismiss()
      self.dialog = None
      print("Edits done!")
   def edit_transaction_dialog(self):
      if not self.dialog:
         self.dialog = MDDialog(
            title="Edit Transactions",
            type="custom",
            content_cls=EditTransactionDialog(),
            buttons=[
               MDFlatButton(
                  text="CANCEL",
                  theme_text_color="Custom",
                  text_color=self.theme_cls.primary_color,
                  on_release=self.cancel_transaction_dialog
               ),
               MDFlatButton(
                  text="OK",
                  theme_text_color="Custom",
                  text_color=self.theme_cls.primary_color,
                  on_release=self.accept_transaction_dialog
               ),
            ],
         )
      self.dialog.open()

