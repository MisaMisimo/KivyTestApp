from datetime import datetime
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.chip import MDChip
from features.storage.StorageInterface import StorageInterface
from utils.utils import DateUtils
# BUG: Can't reopen dialog after dismissing  by touchinng outside of dialog
# TODO: Add ability segmented control to choose beween Expense, Income, CurrentBalance
# TODO: On build, order tags based on how often they are used
# TODO: Add snackbar to to show error whenever inputs aren't valid.
# TODO: Add relationship tags/transaction into database
# TODO: Reset widgets after succesfull add
# TODO: Optimize ViewList LoadTime
Builder.load_file('screens/AddRecordScreen.kv')
class NewTagDialog_BoxLayout(BoxLayout):
   pass
class AddRecordScreen(Screen):
   interfaceStorage = StorageInterface()
   alert_dialog = None
   add_tag_dialog = None
   tag_box_layout = None
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
#               Add Expense Functions
################################################################################
   def cancel_alert_dialog(self, *kwargs):
      self.alert_dialog.dismiss()
      self.alert_dialog = None
   def show_alert_dialog(self, row_dictionary):
      dialog_text = ""
      dialog_text += "Amount: "
      dialog_text += str(row_dictionary['amount']) + "\n"
      dialog_text += "Currrency: "
      dialog_text += str(row_dictionary['currency']) + "\n"
      dialog_text += "Description: "
      dialog_text += str(row_dictionary['description']) + "\n"
      if not self.alert_dialog:
         self.alert_dialog = MDDialog(
               text=dialog_text,
               buttons=[
                  MDFlatButton(
                     text="CANCEL",
                     theme_text_color="Custom",
                     on_release=self.cancel_alert_dialog
                     # text_color=app.theme_cls.primary_color,
                  ),
                  MDFlatButton(
                     text="ACCEPT",
                     theme_text_color="Custom",
                     on_release=self.cancel_alert_dialog
                     # text_color=app.theme_cls.primary_color,
                  ),
               ],
         )
      self.alert_dialog.open()
   def get_validated_inputs(self):
      '''
         Returns None if inputs are not valid.
         Otherwise returns validated inputs
      '''
      def get_record_inputs(self):
         '''
            Gets raw inputs from GUI
         '''
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
      record_input_values = get_record_inputs(self)
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
   def prepare_transaciton_values(self, inputs):
      return {
         "transaction_type" : "expense",
         "amount" : str(inputs["amount"]),
         "currency" : str(inputs["currency"]),
         "description" : str(inputs["description"]),
         "date" : str(inputs["date"]),
         "timestamp" : str(inputs["timestamp"]),
      }
   def write_transaction_tag_relationship_values(self):
      # Get last added Transaction ID
      last_transaction_row = self.interfaceStorage.get_last_item_from_table("transactions")
      # Get tag values
      tag_rows = self.interfaceStorage.get_all_from_table("tags")
      # Get currently selected tags
      selected_tags_text = self.get_selected_tags()
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
      validated_inputs = self.get_validated_inputs()
      if validated_inputs:
         record_outputs = self.prepare_transaciton_values(validated_inputs)
         self.interfaceStorage.insert_into_table("transactions", record_outputs)
         self.write_transaction_tag_relationship_values()
         self.show_alert_dialog(validated_inputs)
      else:
         #TODO add snackbar mentioning an input is not valid
         print("Invalid inputs")

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