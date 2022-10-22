import sqlite3
import sys
import os
from features.storage.config import Tables, CONST
# from constants import Transaction
class StorageInterface():
   def __init__(self):
      pass
   def create_db_directory(self):
      directory_exists =  os.path.isdir(CONST.DATABASE_DIR)
      if(not directory_exists):
         os.mkdir(CONST.DATABASE_DIR)
   def initialize_database(self):
      # Create database directory if it does not yet exist
      self.create_db_directory()
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
   def insert_into_table(self, table_name, attribute_values):
      # Create database or connect to one
      conn = sqlite3.connect(CONST.DATABASE_PATH)
      # Create a cursor
      c = conn.cursor()
      # Add row with Expense values
      sql_cmd_str = "INSERT INTO "
      TableObj = Tables()
      for table in TableObj.configTables:
         if table_name == table.name:
            # Build SQL Command
            sql_cmd_str += table.name + " ( "
            last_attr_indx = len(table.attribute_list)
            attr_indx = 0
            # Iterate through the attributes in the configuration
            for attribute in table.attribute_list:
               # Increase index
               attr_indx += 1
               if not attribute.primary_key:
                  # Build SQL Attributes
                  sql_cmd_str += (attribute.name + " ") 
                  # Add comma if it isn't the last value
                  sql_cmd_str += "," if attr_indx != last_attr_indx else ""
            sql_cmd_str += ") VALUES ( "
            attr_indx = 0
            for attribute in table.attribute_list:
               attr_indx += 1
               if not attribute.primary_key:
                  sql_cmd_str += " "
                  sql_cmd_str += "\'" if(attribute.data_type in TableObj.sql_data_type_uses_tilde) else ""
                  sql_cmd_str += attribute_values[attribute.name]
                  sql_cmd_str += "\'" if(attribute.data_type in TableObj.sql_data_type_uses_tilde) else ""
                  sql_cmd_str += " "
                  # Add comma if it isn't the last value
                  sql_cmd_str += "," if attr_indx != last_attr_indx else ""
            sql_cmd_str += ")"
      print(sql_cmd_str)
      try:
         c.execute(sql_cmd_str)
      except sqlite3.IntegrityError:
         print("Exception caught!")
         print(sys.exc_info()[0])
         print(sys.exc_info()[1])
      conn.commit()
      # Close connection
      conn.close()
   def delete_record(self, key):
      # Connect to database
      # Delete All Rows from Transactions with the key
      # Delete All rows from Tags Where Tranasction Key is the Key
      # Close database
      pass
   def get_table_headers(self, table_name:str):
      # Create database or connect to one
      conn = sqlite3.connect(CONST.DATABASE_PATH)
      # Create a cursor
      c = conn.execute("SELECT * FROM "+table_name)
      # Close connection
      conn.close()
      column_names = list(map(lambda x: x[0], c.description))
      return column_names
   def get_all_from_table(self, table_name:str, amount_limit=10):
      # Create database or connect to one
      conn = sqlite3.connect(CONST.DATABASE_PATH)
      # Create a cursor
      c = conn.cursor()
      c.execute("SELECT * FROM "+table_name + " LIMIT " + str(amount_limit))
      ObjectRow = c.fetchall()
      conn.commit()
      # Close connection
      conn.close()
      return ObjectRow
   def get_all_from_table_order_by(self, table_name:str, column_name:str, desc_asc:str="ASC", amount_limit = 10):
      # Create database or connect to one
      conn = sqlite3.connect(CONST.DATABASE_PATH)
      # Create a cursor
      c = conn.cursor()
      c.execute("SELECT * FROM "+ table_name + " ORDER BY " + column_name +" "+ desc_asc + " LIMIT " + str(amount_limit))
      ObjectRow = c.fetchall()
      conn.commit()
      # Close connection
      conn.close()
      return ObjectRow

