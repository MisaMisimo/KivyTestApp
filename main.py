from kivymd.app import MDApp
from kivy.lang import Builder

from utils.utils import USING_ANDROID_PLTFRM
if(USING_ANDROID_PLTFRM):
   from android.permissions import request_permissions, Permission
   request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
from screens.AddRecordScreen import AddRecordScreen
from screens.ViewRecordScreen import ViewRecordScreen
from screens.ViewGraphsScreen import ViewGraphsScreen

from features.storage.StorageInterface import StorageInterface
class FinanceTrackerApp(MDApp):
   def build(self):
      StorageInterface().initialize_database()
      self.theme_cls.theme_style = "Dark"
      return Builder.load_file('main.kv')
########################################
#     View Record Screen Event
########################################
   def update_list_screen(self):
      self.root.ids['screen2_item'].children[0].ids['selection_list'].update_data_with_last_item()

if __name__ == "__main__":
   FinanceTrackerApp().run()