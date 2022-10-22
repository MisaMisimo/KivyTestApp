from datetime import datetime
from kivy.utils import platform
USING_ANDROID_PLTFRM = (platform == 'android')

class DateUtils():
   def convert_date_format(input_string, input_format, output_format):
      date_time_obj = datetime.strptime(input_string,input_format )
      return datetime.strftime(date_time_obj, output_format)
