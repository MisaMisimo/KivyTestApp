from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from features.storage import StorageInterface

Builder.load_file('screens/AddRecordScreen.kv')
class AddRecordScreen(Screen):
   alert_dialog = None
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
      dialog_text += "Tags: "
      dialog_text += str(row_dictionary['tags']) + "\n"
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
   def write_record_to_db(self):
      # TODO validate all inputs
      try:
         float(self.ids['amount_text_field'].text)
      except ValueError:
         self.ids['amount_text_field'].text = "00.00"
         print("Not a float")
      # Validate Currency
      if (self.ids['currency_field'].current_active_segment == None ):
         currency_str = "MXN"
      else:
         currency_str = str(self.ids['currency_field'].current_active_segment.text)
      tags_list = []
      for tag in self.ids['chip_stack_layout'].children:
         if tag.active == True:
            tags_list.append(tag.text)
      transaction_input_values = {
         "transaction_type": "Expense",
         "amount": float(self.ids['amount_text_field'].text),
         "currency": str(currency_str),
         "description": str(self.ids['description_text_field'].text),
         "date": str(self.ids),
         "tags": tags_list
      }
      interfaceStorage = StorageInterface()
      interfaceStorage.add_record("transactions", transaction_input_values)
      self.show_alert_dialog(transaction_input_values)
   
   #TODO: write tag to database
   #TODO: On build, dislay tags based on database
   #TODO: On build, order tags based on how often they are used


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