from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.chip import MDChip
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from features.storage.StorageInterface import StorageInterface
from utils.utils import DateUtils

from datetime import datetime
Builder.load_file('custom_widgets/TransactionFormWidget.kv')
class NewTagDialog_BoxLayout(MDBoxLayout):
   pass
class TransactionFormWidget(MDBoxLayout):
   add_tag_dialog = None
   interfaceStorage = StorageInterface()
################################################################################
#               Tags Functions
################################################################################
   def write_new_tag_to_db(self, tag_name):
      # Validate TextInput
      row_values = {
         "id": "NULL",
         "name":tag_name,
      }
      self.interfaceStorage.insert_into_table("tags", row_values)
   def cancel_add_tag(self, *kwargs):
      self.add_tag_dialog.dismiss()
      self.add_tag_dialog = None
      self.tag_box_layout = None
   def accept_add_tag(self, *kwargs):
      if self.tag_box_layout:
         self.write_new_tag_to_db(self.tag_box_layout.ids['new_tag_text_field'].text)
         self.load_tags_from_database()
         self.add_tag_dialog.dismiss()
      self.add_tag_dialog = None
      self.tag_box_layout = None
   def show_add_tag_dialog(self, *kwargs):
      if not self.add_tag_dialog:
         self.tag_box_layout = NewTagDialog_BoxLayout()
         self.add_tag_dialog = MDDialog(
            title="New Tag",
            type = "custom",
            content_cls = self.tag_box_layout,
            buttons=[
               MDFlatButton(
                  text="CANCEL",
                  theme_text_color="Custom",
                  on_release=self.cancel_add_tag
               ),
               MDFlatButton(
                  text="ACCEPT",
                  theme_text_color="Custom",
                  on_release=self.accept_add_tag
               ),
            ],
         )
         self.add_tag_dialog.open()
   def get_selected_tags(self):
      rtn_list = []
      for chip_tag in  self.ids['chip_stack_layout'].children:
         if chip_tag.active:
               rtn_list.append(chip_tag.text)
      return rtn_list

################################################################################
#               On load Tags functions
################################################################################
   def load_tags_from_database(self):
      # Clear tags
      self.ids['chip_stack_layout'].clear_widgets()
      # Get table headers
      table_headers = self.interfaceStorage.get_table_headers("tags")
      # Get table values
      tag_rows = self.interfaceStorage.get_all_from_table("tags")
      for row_list in tag_rows:
         self.ids['chip_stack_layout'].add_widget(
            MDChip(
               text = row_list[table_headers.index('name')]
            )
         )
      # Add "+" tag
      add_tag_widget = MDChip(
         text = "+"
      )
      add_tag_widget.bind(
         on_press = self.show_add_tag_dialog
      )
      self.ids['chip_stack_layout'].add_widget(add_tag_widget)
      print("Called on parent")
################################################################################
#               DatePicker Functions
################################################################################
   def my_on_save(self, instance, value, date_range):
      # Update Calendar Button's with selected date
      self.ids['calendar_button'].text = value.strftime("%d/%b/%Y")
   def my_on_cancel(self, instance, value):
      # Do nothing
      pass
   def show_date_picker(self):
      date_dialog = MDDatePicker()
      date_dialog.bind(on_save=self.my_on_save, on_cancel = self.my_on_cancel)
      date_dialog.open()

################################################################################
#               Interface Functions
################################################################################
   def get_form_inputs(self):
      amount = self.ids['amount_text_field'].text
      currency = "MXN" if (self.ids['currency_field'].current_active_segment == None) else self.ids['currency_field'].current_active_segment.text
      description = self.ids['description_text_field'].text
      date = DateUtils.convert_date_format(self.ids['calendar_button'].text, "%d/%b/%Y", "%Y-%m-%d") if (self.ids['calendar_button'].text != "Today") else datetime.now().strftime("%Y-%m-%d")
      timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      record_input_values = {
         "amount":amount,
         "currency": currency,
         "description": description,
         "date": date,
         "timestamp": timestamp,
      }
      return record_input_values
   def get_validated_inputs(self):
      '''
         Returns None if inputs are not valid.
         Otherwise returns validated inputs
      '''
      # record_input_values = get_record_inputs(self)
      record_input_values = self.get_form_inputs()
      # Validate Amount
      try:
         float(record_input_values['amount'])
      except ValueError:
         return None
      # No need to validate currency
      # No need to validate description
      # No need to validate date
      # No need to validate timestamp
      return record_input_values