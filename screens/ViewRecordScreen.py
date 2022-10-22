from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.recycleview import RecycleView
from features.storage.StorageInterface import StorageInterface
from utils.utils import DateUtils
Builder.load_file('screens/ViewRecordScreen.kv')
class ExpenseListItem(TwoLineAvatarIconListItem):
   pass
class ViewRecordRecycleView(RecycleView):
   interfaceStorage = StorageInterface()
   RecycleViewData = []
   def __init__(self, **kwargs):
      super(ViewRecordRecycleView, self).__init__(**kwargs)
      self.load_last_10_items()
      self.data = self.RecycleViewData
   def load_last_10_items(self):
      table_headers = self.interfaceStorage.get_table_headers("transactions")
      last_10_items = self.interfaceStorage.get_all_from_table_order_by("transactions","id","DESC")
      for item in last_10_items:
         self.RecycleViewData.append(
            {
               "text" : str(item[table_headers.index('amount')]) + " " + \
                  item[table_headers.index('currency')] + "   ||   " + \
                  item[table_headers.index('description')],
               "secondary_text": DateUtils.convert_date_format(str(item[table_headers.index('date')]),"%Y-%m-%d","%B %d, %Y")
            }
         )
   def update_data_with_last_item(self):
      table_headers = self.interfaceStorage.get_table_headers("transactions")
      last_row = self.interfaceStorage.get_last_item_from_table("transactions")
      self.RecycleViewData.insert(
         0,
         {
            "text" : str(last_row[table_headers.index('amount')]) + " " + \
                  last_row[table_headers.index('currency')] + "   ||   " + \
                  last_row[table_headers.index('description')],
               "secondary_text": DateUtils.convert_date_format(str(last_row[table_headers.index('date')]),"%Y-%m-%d","%B %d, %Y")
         }
      )
      self.data = self.RecycleViewData


################################################################################
################################################################################
#
#               View Record Screen Class
#
################################################################################
################################################################################
class ViewRecordScreen(Screen):
   interfaceStorage = StorageInterface()
# TODO: Display Amount in float with two decimals
# TODO: Change icon depending on wether it's an expense or an income transaction
# TODO: Swipe to delete
# TODO: Add Topbar navigation to Delete/Edit selected items
# TODO: Add filter/Search  bar on top
# TODO: Display tags based on transaction/tag relationship table
################################################################################
#               On load Record functions
################################################################################

   def on_selected(self, *args):
      pass
   def on_unselected(self, *args):
      pass
   def set_selection_mode(self, *args):
      pass
