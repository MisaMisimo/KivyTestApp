from features.storage.StorageInterface import StorageInterface
from utils.utils import DateUtils
class SearchFilter():
   interfaceStorage = StorageInterface()
   searchResults = None
   begin_date = None
   end_date = None

   def __init__(self, initial_period="Today"):
      self.begin_date, self.end_date = DateUtils.get_dates_from_period(initial_period)
   # We need to input only period filter
   def load_items_in_time_period(self, period_filter="Today", offset = 0):
      # Recalculate begin and end date according to the period filter string
      self.begin_date, self.end_date = DateUtils.get_dates_from_period(period_filter)
      # Get items in specified period
      items_in_time_period = self.interfaceStorage.get_all_from_table_where_date_between(
         "transactions",
         self.begin_date,
         self.end_date
      )
      # Initialize empty return list 
      transaction_info_list = []
      # Iterate through each transaction in specified time period
      for item in items_in_time_period:
         # Get tags related to this transaction
         raw_related_tag_keys = self.interfaceStorage.get_from_table_where_equals(
            "tag_key",
            "transaction_tag_relationship",
            "transaction_key",
            str(item[0])
         )
         # Process raw database output
         related_tag_keys = list(map(lambda x:x[0], raw_related_tag_keys))
         # List to keep track of tags linked to this transact
         related_tag_names = []
         # If we have any related tags
         for related_tag_key in  related_tag_keys:
            # Get names of these tags
            raw_related_tag_name = self.interfaceStorage.get_from_table_where_equals(
               "name",
               "tags",
               "id",
               str(related_tag_key)
            )
            related_tag_names.append(raw_related_tag_name[0][0])
         # Add all this info into dictionary
         transaction_info_list.append(
            {
               "id": item[0],
               "transaction_type": item[1],
               "amount": item[2],
               "currency": item[3],
               "description": item[4],
               "date": item[5],
               "timestamp": item[6],
               "related_tags": related_tag_names,
            }
         )
      return transaction_info_list


"""

Data Structure:
   List for each loaded transction:
      [
         {
            (
               transaction_info =  {
                  "id": item[0],
                  "transaction_type": item[1],
                  "amount":item[2],
                  "currency":item[3],
                  "description":item[4],
                  "date":item[5],
                  "timestamp":item[6],
                  "transaction_tags": []
             )
      ]

"""