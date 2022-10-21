from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarIconListItem
# TODO: Display records as a table
Builder.load_file('screens/ViewRecordScreen.kv')
class ExpenseListItem(TwoLineAvatarIconListItem):
   pass
class ViewRecordScreen(Screen):
   def load_selection_list(self):
      for i in range(10):
         self.ids['selection_list'].add_widget(ExpenseListItem())
   def on_selected(self):
      pass
   def on_unselected(self):
      pass
   def set_selection_mode(self):
      pass
