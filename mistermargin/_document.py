import uuid
from abc import ABCMeta, abstractmethod
from typing import Any, Optional


class Document(metaclass=ABCMeta):
  """
  Documents can record information and even return proccessed data, but they can never act on anything.
  """

  def __init__(self):
    self.id = str(uuid.uuid4())


class Order(Document):

  def __init__(self, account: "Account", type: str, security: str,
               size: float):
    super().__init__()
    self.account = account
    self.type = type
    self.security = security
    self.size = size
    self.is_open = True
    self.is_cancelled = False
    self.trade = None
    self.gtc = True  # Good Til Cancelled

  def checks(self):
    return None

  def __str__(self):
    return (f"Order(type='{self._type}', "
            f"security='{self._security}', size={self._size}, "
            f"is_open={self.is_open})")


class Position(Document):

  def __init__(self, security: str, date, size: float, basis: float):
    self.security = security
    self.open_date = date
    self.size = size
    self.is_open = True

  def __str__(self):
    return (f"Position(security='{self.security}', "
            f"open_date='{self.open_date}', size={self.size}, "
            f"is_open={self.is_open})")


class Trade(Document):

  def __init__(self, date, security, price, size):
    self.execution_date = date
    self.security = security
    self.price = price
    self.size = size
    self.basis = price * size

  def __str__(self):
    return (f"Trade(execution_date='{self.execution_date}', "
            f"security='{self.security}', price={self.price})"
            f"size={self.size}, cost={self.basis}")

