from utils.utils import USING_ANDROID_PLTFRM
import os
class CONST():
      if(USING_ANDROID_PLTFRM):
         from android.storage import primary_external_storage_path
         DATABASE_DIR = primary_external_storage_path()+'/database/'
      else:
         DATABASE_DIR = os.getcwd()+'/database/'
      DATABASE_FILE_NAME = "finances.db"
      DATABASE_PATH = DATABASE_DIR + DATABASE_FILE_NAME
class Tables():
   class Attribute():
      def __init__(
         self,
         name,
         data_type,
         primary_key = False,
         not_null = False,
         unique = False,
         check = False,
         check_str = ""):
         self.name = name
         self.data_type = data_type
         # Constraints
         self.primary_key = primary_key
         self.not_null = not_null
         self.unique = unique
         self.check = check
         self.check_str = check_str
   class Table():
      def __init__(self, name, attribute_list):
         self.name = name
         self.attribute_list = attribute_list
      def add_attribute(self, attribute):
         self.attribte_list.append(attribute)

   configTables = [
      Table(name = "transactions",
         attribute_list = [
            Attribute(name = "transaction_id",  data_type = "integer",                primary_key = True),
            Attribute(name = "transaction_type",data_type = "integer"),
            Attribute(name = "amount",          data_type = "decimal(65,2)"),
            Attribute(name = "currency",        data_type = "integer"),
            Attribute(name = "description",     data_type = "text"),
            Attribute(name = "date",            data_type = "date"),
            Attribute(name = "timestamp",       data_type = "timestamp"),
         ]
      ),
      Table(name = "tags",
         attribute_list = [
            Attribute(name = "tag_id",          data_type = "integer", primary_key = True),
            Attribute(name = "name",            data_type = "text", unique = True),
         ]
      ),
      Table(name = "transaction_tag_relationship",
         attribute_list = [
            Attribute(name = "relation_key",    data_type = "integer", primary_key = True),            
            Attribute(name = "transaction_key", data_type = "integer"),            
            Attribute(name = "tag_key",         data_type = "integer"),
         ]
      )
   ]
