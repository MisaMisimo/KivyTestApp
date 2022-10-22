from kivymd.uix.textfield import MDTextField
import re
class MDFloatTextField(MDTextField):
   # Pattern is anything that's not a number
   not_a_number_pat = re.compile('[^[0-9]|[^A-Z]|[^a-z]|[^ ]')
   def insert_text(self, substring, from_undo=False):
      # if there is a dot
      if '.' in self.text:
         # find dot position
         dot_position = self.text.index('.')
         # and cursor if cursor two digits after the dots
         if self.cursor[0] > dot_position + 2 :
            # ignore incoming strings
            s = ''

      return super().insert_text(s, from_undo=from_undo)