from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarIconListItem
from features.storage.StorageInterface import StorageInterface
from utils.utils import DateUtils
Builder.load_file('screens/ViewRecordScreen.kv')
class ExpenseListItem(TwoLineAvatarIconListItem):
   pass
class ViewRecordScreen(Screen):
   interfaceStorage = StorageInterface()
################################################################################
#               On load Record functions
################################################################################
   def load_selection_list(self):
      # Empty the list
      self.ids['selection_list'].clear_widgets()
      # Add each list item from database
      # Get table headers
      table_headers = self.interfaceStorage.get_table_headers("transactions")
      transaction_rows = self.interfaceStorage.get_all_from_table("transactions")
      number_of_items = 0
      for row_list in transaction_rows:
         self.ids['selection_list'].add_widget(
            ExpenseListItem(
               text = str(row_list[table_headers.index('amount')]) + " " + \
                  row_list[table_headers.index('currency')] + "   ||   " + \
                  row_list[table_headers.index('description')],
               secondary_text =  DateUtils.convert_date_format(str(row_list[table_headers.index('date')]),"%Y-%m-%d","%B %d, %Y")
            )
         )
         number_of_items += 1
   def on_selected(self, *args):
      pass
   def on_unselected(self, *args):
      pass
   def set_selection_mode(self, *args):
      pass
