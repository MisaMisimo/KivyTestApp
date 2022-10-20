import sqlite3
from features.storage.config import Tables, CONST
# from constants import Transaction
class StorageInterface():
   def __init__(self):
      pass
   def initialize_database(self):
      # Create database or connect to one
      conn = sqlite3.connect(CONST.DATABASE_PATH)
      # Create a cursor
      c = conn.cursor()
      # Create a table that don't yet exist
      for table in Tables().configTables:
         # Build SQL Command
         sql_cmd_str = " CREATE TABLE if not exists " + table.name + "(\n"
         # Temp variables to assist with iterating through the attribute list
         last_attr_indx = len(table.attribute_list)
         attr_indx = 0
         for attribute in table.attribute_list:
            # Increase index
            attr_indx += 1
            # Build SQL Attributes
            sql_cmd_str += "   " + attribute.name + " " + attribute.data_type
            sql_cmd_str += " primary key autoincrement" if attribute.primary_key else ""
            sql_cmd_str += " not null" if attribute.not_null else ""
            sql_cmd_str += " unique" if attribute.unique else ""
            sql_cmd_str += (" check(" + attribute.check_str+ ")" ) if attribute.check else ""
            # If it's the last attribute, don't add a comma
            sql_cmd_str += "," if (attr_indx < last_attr_indx) else ""
            sql_cmd_str += "\n"
         # Need call sql command to actually crete table
         sql_cmd_str += ")\n"
         c.execute(sql_cmd_str)
         conn.commit()
      # Close connection
      conn.close()
   def add_record(self, table_name, attribute_values):
      # Create database or connect to one
      conn = sqlite3.connect(CONST.DATABASE_PATH)
      # Create a cursor
      c = conn.cursor()
      # Add row with Expense values
      sql_cmd_str = "INSERT INTO "
      for table in Tables().configTables:
         if table_name == table.name:
            # Build SQL Command
            sql_cmd_str += table.name + " ("
            last_attr_indx = len(table.attribute_list)
            attr_indx = 0
            # Iterate through the attributes in the configuration
            for attribute in table.attribute_list:
               # Increase index
               attr_indx += 1
               # Build SQL Attributes
               sql_cmd_str += (attribute.name + " ") if not attribute.primary_key else ""
            sql_cmd_str += ") VALUES (\'"
            sql_cmd_str += attribute_values[attribute.name]
            sql_cmd_str += "\')"
      print(sql_cmd_str)
      c.execute(sql_cmd_str)
      conn.commit()
      # Close connection
      conn.close()
   def delete_record(self, key):
      # Connect to database
      # Delete All Rows from Transactions with the key
      # Delete All rows from Tags Where Tranasction Key is the Key
      # Close database
      pass
   def get_transactions(self,max_rows = 100):
      # 
      pass
   

