# from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from screens.AddRecordScreen import AddRecordScreen
from screens.ViewRecordScreen import ViewRecordScreen

class FinanceTrackerApp(MDApp):
   def build(self):   
    return Builder.load_file('main.kv')

if __name__ == "__main__":
   FinanceTrackerApp().run()