from enum import Enum, auto
from datetime import datetime
class TransactionTypeEnum(Enum):
   e_EXPENSE = auto()
   e_INCOME = auto()
class Transaction():
   def __init__(self, transaction_type, amount, description, date):
      self.transaction_type = transaction_type
      self.amount = amount
      self.description = description
      self.date = date
      self.timestamp = datetime.now()

