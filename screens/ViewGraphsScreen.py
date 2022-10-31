from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd_extensions.akivymd.uix.charts import AKPieChart
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from features.searchfilter.searchfilter import SearchFilter
Builder.load_file('screens/ViewGraphsScreen.kv')
class ViewGraphsScreen(Screen):
   searchFilter = None
   period_filter = None
   def __init__(self, **kw):
      super(ViewGraphsScreen, self).__init__(**kw)
      self.searchFilter = SearchFilter()
      self.update_displayed_search_dates()
   def update_period_filter(self):
      # If it exists, reset the pie chart
      try:
         self.ids['pchart'].remove_widget(self.piechart)
         self.ids['psummary'].remove_widget(self.summary_table)
      except AttributeError:
         pass
      # Get current time-period filter
      try:
         # This may fail on load, since it is called before evertynign is properly loaded.
         self.period_filter = self.ids['period_carousel'].current_slide.text
      except AttributeError:
         # Use default value if it s not yet created.
         self.period_filter = "Today"
         # Update items according to period filter
         self.pie_items = [self.searchFilter.load_piechart_items(self.period_filter)]
   def update_displayed_search_dates(self):
      # Update filter dates in screen
      try:
         # This may fail on load, since it is called before evertynign is properly loaded.
         self.ids['begin_date_button'].text = self.searchFilter.begin_date.strftime("%a %b %d %Y")
         self.ids['end_date_button'].text   = self.searchFilter.end_date.strftime("%a %b %d %Y")
      except (AttributeError, KeyError):
         # If it's not loaded, the *.kv file takes care of the initial text
         pass
   def draw_chart(self):
      self.update_period_filter()
      self.pie_items = [self.searchFilter.load_piechart_items(self.period_filter)]
      # If we don't have an error on the first element??
      if self.pie_items[0]:
         self.piechart = AKPieChart(
            items=self.pie_items, 
            size_hint=[0.9,0.9],
         )
      else:
         self.piechart = MDLabel(
            text = "No Results",
            halign = "center"
         )
      
      self.ids['pchart'].add_widget(self.piechart)

   def draw_summary_table(self):
      # Need to fix this, since update_period_filter removes the other iwdgte it must only be casled once
      # self.update_period_filter()
      table_row_data = self.searchFilter.load_summary_chart(self.period_filter)
      table_colum_data = [
         ("Type", dp(30)),
         ("Tag", dp(30)),
         ("Amount", dp(30)),
         ("Percent", dp(30)),
      ]
      if (table_row_data):
         self.summary_table = MDDataTable(
            size_hint = (1,1),
            column_data = table_colum_data,
            row_data = table_row_data
         )
      else:
         self.summary_table = MDLabel(
            text = "No Results",
            halign = "center",
         )
      self.ids['psummary'].add_widget(self.summary_table)
      print(table_row_data)

