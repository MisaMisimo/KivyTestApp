from kivymd.app import MDApp
from kivy.lang import Builder

from screens.AddRecordScreen import AddRecordScreen
from screens.ViewRecordScreen import ViewRecordScreen
from screens.ViewGraphsScreen import ViewGraphsScreen

from features.storage import StorageInterface
class FinanceTrackerApp(MDApp):
   def build(self):
      StorageInterface().initialize_database()
      self.theme_cls.theme_style = "Dark"
      return Builder.load_file('main.kv')

if __name__ == "__main__":
   FinanceTrackerApp().run()