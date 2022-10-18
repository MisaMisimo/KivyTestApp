from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.pickers import MDDatePicker
Builder.load_file('screens/AddRecordScreen.kv')
class AddRecordScreen(Screen):
   def my_on_save(self, instance, value, date_range):
      # Update Calendar Button's with selected date
      self.ids['calendar_button'].text = value.strftime("%d/%b/%Y")
   def my_on_cancel(self, instance, value):
      # Do nothing
      pass
   def show_date_picker(self):
      date_dialog = MDDatePicker()
      date_dialog.bind(on_save=self.my_on_save, on_cancel = self.my_on_cancel)
      date_dialog.open()