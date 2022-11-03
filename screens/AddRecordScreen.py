from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import BoxLayout
from features.storage.StorageInterface import StorageInterface
# from custom_widgets.TransactionFormWidget import TransactionFormWidget
# BUG: Can't reopen dialog after dismissing  by touchinng outside of dialog
# TODO: Add ability segmented control to choose beween Expense, Income, CurrentBalance
# TODO: On build, order tags based on how often they are used
# TODO: Add snackbar to to show error whenever inputs aren't valid.
# TODO: Add relationship tags/transaction into database
# TODO: Reset widgets after succesfull add
# TODO: Optimize ViewList LoadTime
Builder.load_file('screens/AddRecordScreen.kv')
class AddRecordScreen(Screen):
   interfaceStorage = StorageInterface()
   alert_dialog = None
   tag_box_layout = None
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
   
   def prepare_transaction_values(self, inputs):
      return {
         "transaction_type" : str(inputs["transaction_type"]),
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
         self.interfaceStorage.insert_into_table("transactions", record_outputs)
         self.write_transaction_tag_relationship_values()
         self.show_alert_dialog(validated_inputs)
      else:
         #TODO add snackbar mentioning an input is not valid
         print("Invalid inputs")
