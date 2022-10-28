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
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty
from utils.utils import DateUtils
from features.storage.StorageInterface import StorageInterface

LONG_PRESSED_TIME = 0.6  # Change time in seconds
Builder.load_file('custom_widgets/selectablelistitem.kv')
class EditTransactionPopup(MDBoxLayout):
   interfaceStorage = StorageInterface()

   def __init__(self, transaction_info=None, *args, **kwargs):
      super().__init__(*args, **kwargs)
      if transaction_info:
         self.transaction_info = transaction_info
         self.ids['transaction_form'].ids['amount_text_field'].text = "{:.2f}".format(float(transaction_info['amount']))
         self.ids['transaction_form'].ids['description_text_field'].text = str(transaction_info['description'])
         self.ids['transaction_form'].ids['calendar_button'].text = DateUtils.convert_date_format(transaction_info['date'], "%Y-%m-%d", "%d/%b/%Y")
         self.children[1].set_selected_currency(str(transaction_info['currency']))
   def accept_transaction_changes(self):
      self.process_expense_inputs()
   def write_transaction_tag_relationship_values(self):
      # Get last added Transaction ID
      last_transaction_row = self.interfaceStorage.get_last_item_from_table("transactions")
      # Get tag values
      tag_rows = self.interfaceStorage.get_all_from_table("tags")
      # Get currently selected tags
      selected_tags_text = self.ids['transaction_form'].get_selected_tags()
      # Get IDs for the current selected tags
      selected_tag_ids = []
      for selected_tag_text in selected_tags_text:
         for tag_row in tag_rows:
            if selected_tag_text == tag_row[1]:
               selected_tag_ids.append(tag_row[0])
               break
      # Prepare outputs
      for selected_tag_id in selected_tag_ids:
         record_outputs = {
               "id": "NULL",
               "transaction_key": str(last_transaction_row[0]),
               "tag_key": str(selected_tag_id),
            }
         self.interfaceStorage.insert_into_table("transaction_tag_relationship", record_outputs)
   def process_expense_inputs(self):
      # TODO validate all inputs
      validated_inputs = self.ids['transaction_form'].get_validated_inputs()
      if validated_inputs:
         record_outputs = self.prepare_transaction_values(validated_inputs)
         self.interfaceStorage.update_set_by_id("transactions", record_outputs, self.transaction_info['id'])
         # self.write_transaction_tag_relationship_values()
         # self.show_alert_dialog(validated_inputs)
      else:
         #TODO add snackbar mentioning an input is not valid
         print("Invalid inputs")
   def prepare_transaction_values(self, inputs):
      return {
         "transaction_type" : "expense",
         "amount" : str(inputs["amount"]),
         "currency" : str(inputs["currency"]),
         "description" : str(inputs["description"]),
         "date" : str(inputs["date"]),
         "timestamp" : str(inputs["timestamp"]),
      }
class SelectableListItem(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
   index = None
   long_press_threshold_reached = False
   long_press_event = None
   transaction_popup = None
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
      print("Long press on transaction Values " + str(self.transaction_info))
      self.edit_transaction_popup()
   def cancel_transaction_popup(self, *kwargs):
      self.transaction_popup.dismiss()
      self.transaction_popup = None
   def accept_transaction_popup(self, *kwargs):
      self.transaction_popup.dismiss()
      self.transaction_popup = None
      print("Edits done!")
   def edit_transaction_popup(self):
      if not self.transaction_popup:
         self.transaction_popup = Popup(
            title="Edit Transaction",
            content=EditTransactionPopup(transaction_info=self.transaction_info),
            auto_dismiss=False,
         )
         self.transaction_popup.bind(on_dismiss = self.popup_dismissed)
      self.transaction_popup.open()
   def  popup_dismissed(self, *kwargs):
      pass
       
