import uuid

from mistermargin.account import Account
from mistermargin.mister import MisterMarket

from ._agent import Agent
from ._document import Trade, Position


class Broker(Agent):

  def __init__(self):
    super().__init__()
    self.commission = 0
    self.market: "MisterMarket"
    self.type = "normal"
    self.clients = []
    self.accounts = []

  def data(self):
    pass

  def next(self):
    self.check_accounts()
    self.check_orders()

  def add_market(self, market: "MisterMarket"):
    self.market = market

  def add_client(self, client: "Client"):
    client.broker = self
    # Add the client to our client list
    self.clients.append(client)
    # And sign them up for an account
    self.market.create_account(self, client, client.starting_cash)

  def add_account(self, account: "Account"):
    self.accounts.append(account)

  def check_accounts(self):
    for account in self.accounts:
      account.generate_report()

  def generate_trade(self, order: "Order"):
    today_date = self.market.feed.indice
    price = self.market.feed[order.security][0]['Close']
    trade = Trade(today_date, order.security, price, order.size)
    order.trade = trade
    order.account.trade_history.append(trade)

  def open_position(self, order: "Order"):
    position = Position(order.security, order.trade.execution_date, order.size, order.trade.basis)
    order.account.positions.append(position)
    order.account.securities.add(order.security)

  def conduct_transaction(self, order: "Order"):
    order.account.cash -= order.trade.basis
  
  def is_valid_order(self, order: "Order"):
    return order.size <= order.account.cash

  def execute_order(self, order: "Order"):
    self.generate_trade(order)
    self.open_position(order)
    self.conduct_transaction(order)
    self.close_order(order)

  def close_order(self, order: "Order"):
    order.is_open = False
    order.account.open_orders.remove(order)
    order.account.closed_orders.append(order)

  def cancel_order(self, order: "Order"):
    order.is_open = False
    order.is_cancelled = True
    order.account.open_orders.remove(order)
    order.account.canceled_orders.append(order)

  def check_orders(self):
    for account in self.accounts:
      for order in account.open_orders:
        if self.is_valid_order(order):
          self.execute_order(order)
        else:
          self.cancel_order(order)
