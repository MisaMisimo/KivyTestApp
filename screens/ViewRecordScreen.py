from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleboxlayout import  RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.recycleview import RecycleView
from features.storage.StorageInterface import StorageInterface
from utils.utils import DateUtils
from kivy.properties import BooleanProperty
Builder.load_file('screens/ViewRecordScreen.kv')
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
   """
   Adds  selection and focus behavior to the view
   """
   pass
class ViewRecordRecycleView(RecycleView):
   interfaceStorage = StorageInterface()
   RecycleViewData = []
   period_filter = "Weekly"
   def __init__(self, **kwargs):
      super(ViewRecordRecycleView, self).__init__(**kwargs)
      self.load_items_in_time_period()
      self.data = self.RecycleViewData
   def load_items_in_time_period(self):
      try:
         # This may fail on load, since it is called before evertynign is properly loaded.
         self.period_filter = self.parent.parent.ids['period_carousel'].current_slide.text
      except AttributeError:
         # Use default value if it s not yet created.
         self.period_filter = "Today"
      begin_date, end_date = DateUtils.get_dates_from_period(self.period_filter)
      # Update filter dates in screen
      try:
         # This may fail on load, since it is called before evertynign is properly loaded.
         self.parent.parent.ids['begin_date_button'].text = begin_date.strftime("%a %b %d %Y")
         self.parent.parent.ids['end_date_button'].text   = end_date.strftime("%a %b %d %Y")
      except AttributeError:
         pass
      table_headers = self.interfaceStorage.get_table_headers("transactions")
      items_in_time_period = self.interfaceStorage.get_all_from_table_where_date_between("transactions",begin_date, end_date)
      tags = self.interfaceStorage.get_all_from_table("tags")
      self.RecycleViewData = []
      for item in items_in_time_period:
         # Get tags related to this transaction
         related_tag_keys = self.interfaceStorage.get_from_table_where_equals("tag_key", "transaction_tag_relationship", "transaction_key", str(item[0]) )
         transaction_tags = []
         for related_tag in  related_tag_keys:
            for tag in tags:
               if related_tag[0] == tag[0]:
                  transaction_tags.append(tag[1])
                  break
         first_string = "{:.2f}".format(item[table_headers.index('amount')]) + " " + \
                  item[table_headers.index('currency')] + "   ||   " + \
                  item[table_headers.index('description')]
         second_string = DateUtils.convert_date_format(str(item[table_headers.index('date')]),"%Y-%m-%d","%B %d, %Y") + \
                  "      "
         transaction_info = {
            "id": item[0],
            "transaction_type": item[1],
            "amount":item[2],
            "currency":item[3],
            "description":item[4],
            "date":item[5],
            "timestamp":item[6],
         }
         for tag in transaction_tags:
            second_string += " |" + tag + "| "
         self.RecycleViewData.append(
            {
               "text" : first_string,
               "secondary_text": second_string,
               "transaction_info": transaction_info
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
