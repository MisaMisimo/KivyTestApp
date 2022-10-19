# from constants import Transaction
class StorageInterface():
   def __init__(self):
      pass
   def reinitialize_database(self):
      pass
   def add_expense_record(self, row_dictionary):
      # Connect to database
      # Add row with Expense values
      # Close database
      pass
   def delete_record(self, key):
      # Connect to database
      # Delete All Rows from Transactions with the key
      # Delete All rows from Tags Where Tranasction Key is the Key
      # Close database
      pass
   def get_transactions(self,max_rows = 100):
      # 
      pass
   

