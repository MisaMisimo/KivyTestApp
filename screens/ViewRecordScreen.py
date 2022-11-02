from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleboxlayout import  RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.recycleview import RecycleView
from features.storage.StorageInterface import StorageInterface
from features.searchfilter.searchfilter import SearchFilter
from kivy.properties import BooleanProperty
from utils.utils import DateUtils
Builder.load_file('screens/ViewRecordScreen.kv')
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
   """
   Adds  selection and focus behavior to the view
   """
   pass
class ViewRecordRecycleView(RecycleView):
   RecycleViewData = []
   period_filter = "Today"
   begin_date = None
   end_date = None
   interfaceStorage = None
   searchFilter = None
   def __init__(self, **kwargs):
      super(ViewRecordRecycleView, self).__init__(**kwargs)
      # Initialize search filter
      self.searchFilter = SearchFilter("Today")
      # Update shown search dates
      self.update_displayed_search_dates()
      self.load_items_into_recycleview_list()
   def update_period_filter(self):
      # Get current time-period filter
      try:
         # This may fail on load, since it is called before evertynign is properly loaded.
         self.period_filter = self.parent.parent.ids['period_carousel'].current_slide.text
      except AttributeError:
         # Use default value if it s not yet created.
         self.period_filter = "Today"
   def update_displayed_search_dates(self):
      # Update filter dates in screen
      try:
         # This may fail on load, since it is called before evertynign is properly loaded.
         self.parent.parent.ids['begin_date_button'].text = self.searchFilter.begin_date.strftime("%a %b %d %Y")
         self.parent.parent.ids['end_date_button'].text   = self.searchFilter.end_date.strftime("%a %b %d %Y")
      except AttributeError:
         # If it's not loaded, the *.kv file takes care of the initial text
         print("Problem Setting Dates due to Attribute Error. i.e. components not loaded yet.")
         pass
   def load_items_into_recycleview_list(self):
      self.update_period_filter()
      # Get items in this period
      items_in_time_period = self.searchFilter.load_items_in_time_period(
         period_filter = self.period_filter,
         offset = 0
      )
      # Empty the recycle view data
      self.RecycleViewData = []
      # Iterate through transactions in this time period
      for item in items_in_time_period:
         # Build First String for recycle view item
         first_string = "{:.2f}".format(item['amount']) + " " + \
            item['currency'] + "   ||   " + item['description']
         # Build Second String for recycle view item
         second_string = DateUtils.convert_date_format(str(item['date']),"%Y-%m-%d","%B %d, %Y")
         for tag in item['related_tags']:
            second_string += " |" + tag + "| "
         self.RecycleViewData.append(
            {
               "text" : first_string,
               "secondary_text": second_string,
               "transaction_info": item,
               "transaction_tags": item['related_tags'],
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

