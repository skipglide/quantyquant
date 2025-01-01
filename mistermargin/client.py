from abc import abstractmethod
from typing import Any

from mistermargin.mister import MisterMarket

from ._agent import Agent
from ._document import Order


class Client(Agent):

  def __init__(self):
    super().__init__()
    self.market: "MisterMarket"
    self.account: "Account"
    self.starting_cash:int = 1000
    self.broker: "Broker"

  def __str__(self):
    return f"Client(id={self.id}, broker={self.account.broker.id}, account={self.account.id})"

  def add_market(self, market: "MisterMarket"):
    self.market = market

  def create_order(self, type: str, security: str, commision=0.0, cash=0.0, size=0.0):
    match type:
      case 'market_buy':
        value = cash * (1 - commision)
        price = self.feed[security][0]['Close']
        size = value / price
        order = Order(self.account, type, security, size)
        self.account.add_order(order)
      case 'market_sell':
        value = cash * (1 - commision)
        price = self.feed[security][0]['Close']
        size = size
        order = Order(self.account, type, security, size)
        self.account.add_order(order)
  
  def buy(self, security, cash):
    commision = self.broker.commission
    self.create_order(type='market_buy', cash=cash, commision=commision, security=security)

  def sell(self, security, size):
    commision = self.broker.commission
    break
    # You need to make it where the order logic executed by the broken handles both buying and selling, tehe
    self.create_order(type = 'market_sell', size=size, commision=commision, security=security)

  def give_account(self, account):
    self.account = account
