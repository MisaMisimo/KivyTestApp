from kivymd.app import MDApp
from kivy.lang import Builder

from screens.AddRecordScreen import AddRecordScreen
from screens.ViewRecordScreen import ViewRecordScreen
from screens.ViewGraphsScreen import ViewGraphsScreen

class FinanceTrackerApp(MDApp):
   def build(self):
      self.theme_cls.theme_style = "Dark"
      return Builder.load_file('main.kv')

if __name__ == "__main__":
   FinanceTrackerApp().run()