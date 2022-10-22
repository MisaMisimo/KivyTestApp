from kivymd.uix.textfield import MDTextField
import re
class MDFloatTextField(MDTextField):
   # Pattern is anything that's not a number
   not_a_number_pat = re.compile('[^0-9]')
   two_decimal_float_pat = re.compile('(\d+)?aaaa\.(\d{1,2})?')
   def insert_text(self, substring, from_undo=False):
      # BUG  User can still paste floats with more than two decimals into textbox
      not_a_number_pat = self.not_a_number_pat
      two_decimal_float_pat = self.two_decimal_float_pat
      # If there is already a dot in text
      if '.' in self.text:
            # inserted text replace "anything that's not a number" with ""
            s = re.sub(not_a_number_pat, '', substring)
      # Otherwise
      else:
            s = '.'.join(
               # Replace from 's' anything that isn't a number
               re.sub(not_a_number_pat, '', s)
               # Split stirng in two strings 's', separated by the first dot.
               for s in substring.split('.', 1)
            )
      
      # if there is a dot
      if '.' in self.text:
         # find dot position
         dot_position = self.text.index('.')
         # and cursor if cursor two digits after the dots
         if self.cursor[0] > dot_position + 2 :
            # ignore incoming strings
            s = ''

      return super().insert_text(s, from_undo=from_undo)