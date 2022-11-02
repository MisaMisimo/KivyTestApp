from datetime import datetime, timedelta
from kivy.utils import platform
from dateutil.relativedelta import relativedelta
USING_ANDROID_PLTFRM = (platform == 'android')

class DateUtils():
   def convert_date_format(input_string, input_format, output_format):
      date_time_obj = datetime.strptime(input_string,input_format )
      return datetime.strftime(date_time_obj, output_format)
   def get_dates_from_period(period="Today", offset = 0):
      today = datetime.today()
      begin_date = today
      end_date = today
      if period == "Weekly":
         # Calculate with 0 Offset
         begin_date = today - timedelta(days = today.weekday())
         end_date = begin_date + timedelta(days = 6)
         # 
         begin_date = begin_date + timedelta(weeks=offset)
         end_date = end_date + timedelta(weeks=offset)
      elif period == "Fortnight":
         current_fortnight_is_first = True
         if today.day < 16:
            current_fortnight_is_first = True
            # If it's before 16
            #     begin date should be same month, day1.
            #     End date should be same mont, day15
            #  Else:
            #     begin date should be same month, day 16
            #     end date should be same month day 30
            begin_date = today - timedelta(days = (today.day - 1 ) )
            end_date = begin_date + timedelta(days= 15 - 1)
         else:
            current_fortnight_is_first = False
            begin_date = today - timedelta(days= (today.day - 15))
            end_date = datetime(today.year + today.month // 12, today.month % 12 + 1, 1) - timedelta(1)
         offset_is_whole_month = ( (offset % 2) == 0 )
         # Apply Offset
         begin_date += relativedelta(months=offset//2)
         end_date += relativedelta( months=offset//2)
         if current_fortnight_is_first and not offset_is_whole_month:
            begin_date += relativedelta(days = 15)
            end_date += relativedelta(days = 15)

      elif period == "Monthly":
         begin_date = today - timedelta(days = today.day - 1)
         end_date = datetime(today.year + today.month // 12, today.month % 12 + 1, 1) - timedelta(1)
         # Apply Offset
         begin_date += relativedelta(months=offset)
         end_date += relativedelta(months=offset)
      elif period == "Today":
         # TODO: Write Logic for quarterl period
         # Apply Offset
         begin_date = begin_date + timedelta(days=offset)
         end_date = end_date + timedelta(days=offset)
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