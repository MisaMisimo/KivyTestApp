from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.chip import MDChip

from features.storage import StorageInterface
# FIXME: Can't reopen dialog after dismissing  by touchinng outside of dialog
# TODO: On build, order tags based on how often they are used
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
      # Add each tag from database
      for tag_name in self.interfaceStorage.get_tag_names():
         self.ids['chip_stack_layout'].add_widget(
            MDChip(
               text = tag_name
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
      dialog_text += "Tags: "
      dialog_text += str(row_dictionary['tags']) + "\n"
      if not self.alert_dialog:
         # TODO: Move this Dialog to it's own file
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
      self.interfaceStorage.add_record("transactions", transaction_input_values)
      self.show_alert_dialog(transaction_input_values)

################################################################################
#               Tag Functions
################################################################################
   def write_new_tag_to_db(self, tag_name):
      # Validate TextInput
      row_values = {
         "tag_id": "NULL",
         "name":tag_name,
      }
      self.interfaceStorage.add_record("tags", row_values)
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