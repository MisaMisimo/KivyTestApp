from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd_extensions.akivymd.uix.charts import AKPieChart
from kivy.metrics import dp
Builder.load_file('screens/ViewGraphsScreen.kv')
class ViewGraphsScreen(Screen):
   def __init__(self, **kw):
      super(ViewGraphsScreen, self).__init__(**kw)
   def draw_chart(self):
      self.items = [{
         "Electronics": 40,
         "Laptops": 20,
         "Shoes": 20,
         "iPhones": 20
      }]
      self.piechart = AKPieChart(
         items=self.items, 
         size_hint=[0.9,0.9],
      )
      self.ids['pchart'].add_widget(self.piechart)
   def print_button_text(self):
      print("Hello")