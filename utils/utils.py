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

class MathUtils():
   def weights_to_percent(weight_dict:dict):
      # Calculate total amount
      total_amount = 0
      for key in weight_dict:
         total_amount += weight_dict[key]
      # Get percentages
      percent_dict = {}
      # Avoid dividing by zero
      if total_amount != 0:
         for k,v in weight_dict.items():
            percent_dict[k] = (v * 100 ) / total_amount
      integer_percents  = MathUtils.largestRemainder(percent_dict)

      return integer_percents
      
   def largestRemainder(float_percents_dict:dict):
      # Take all the integer parts
      int_percent_dict = {}
      remainder_percent_list = {}
      amount_to_distribute = 100
      for key, value  in float_percents_dict.items():
         int_percent_dict[key] = int(value)
         remainder_percent_list[key] = value - int(value)
         amount_to_distribute -= int(value)

      # Distribute remainder in order of the highest remainders
      for key, value in sorted(
         remainder_percent_list.items(),
         key = lambda item: item[1]
         ):
         if amount_to_distribute > 0:
            int_percent_dict[key] += 1
            amount_to_distribute -= 1
         else:
            break
      return int_percent_dict