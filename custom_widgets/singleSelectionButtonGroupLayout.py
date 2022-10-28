from kivymd.uix.boxlayout import MDBoxLayout
class SingleSelectionButtonGroupLayout(MDBoxLayout):
   def __init__(self, button_data, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.button_data = button_data
      Button