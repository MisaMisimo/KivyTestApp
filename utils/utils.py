from datetime import datetime, timedelta
from kivy.utils import platform
USING_ANDROID_PLTFRM = (platform == 'android')

class DateUtils():
   def convert_date_format(input_string, input_format, output_format):
      date_time_obj = datetime.strptime(input_string,input_format )
      return datetime.strftime(date_time_obj, output_format)
   def get_dates_from_period(period="Today"):
      today = datetime.today()
      begin_date = today
      end_date = today
      if period == "Weekly":
         begin_date = today - timedelta(days = today.weekday())
         end_date = begin_date + timedelta(days = 6)
      elif period == "Fortnight":
         if today.day < 16:
            # If it's before 16
            #     begin date should be same month, day1.
            #     End date should be same mont, day15
            #  Else:
            #     begin date should be same month, day 16
            #     end date should be same month day 30
            begin_date = today - timedelta(days = today.day + 1)
            end_date = begin_date + timedelta(days= 14)
         else:
            begin_date = today - timedelta(days= (today.day - 15))
            end_date = datetime(today.year + today.month // 12, today.month % 12 + 1, 1) - timedelta(1)
      elif period == "Monthly":
         begin_date = today - timedelta(days = today.day - 1)
         end_date = datetime(today.year + today.month // 12, today.month % 12 + 1, 1) - timedelta(1)
      elif period == "Today":
         # TODO: Write Logic for quarterl period
         pass
      print("-------------------")
      print("Begin date:", begin_date)
      print("End   date:", end_date)
      print("-------------------")
      return(begin_date, end_date)

