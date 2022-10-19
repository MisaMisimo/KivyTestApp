class Tables():
   class Transactions():
      def __init__(self, transaction_type, amount, description, date):
         self.transaction_type = transaction_type
         self.amount = amount
         self.description = description
         self.date = date
         self.timestamp = datetime.now()

   class Tags():
      def __init__(self, name):
         self.name = name
   
   class TransactionTagRelationShip():
      def __init__(self, transaction_key, tag_key):
         self.transaction_key = transaction_key
         self.tag_key = tag_key
