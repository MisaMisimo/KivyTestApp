from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd_extensions.akivymd.uix.charts import AKPieChart
from kivy.metrics import dp
from features.searchfilter.searchfilter import SearchFilter
Builder.load_file('screens/ViewGraphsScreen.kv')
class ViewGraphsScreen(Screen):
   searchFilter = None
   def __init__(self, **kw):
      super(ViewGraphsScreen, self).__init__(**kw)
      self.searchFilter = SearchFilter()
   def draw_chart(self):
      self.pie_items = [self.searchFilter.load_piechart_items()]
      self.piechart = AKPieChart(
         items=self.pie_items, 
         size_hint=[0.9,0.9],
      )
      self.ids['pchart'].add_widget(self.piechart)
   def print_button_text(self):
      print("Hello")