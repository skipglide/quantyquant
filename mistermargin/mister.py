from typing import Any

from pandas import DataFrame

from .account import Account


class MisterMarket:

  def __init__(self) -> None:
    self.feed: "Feed"
    self.brokers = []
    self.clients = []
    self.accounts = []
    self.last_day: Any

  def next(self):
    for client in self.clients:
      client.next()

  def add_broker(self, broker: "Broker"):
    broker.add_market(self)
    self.brokers.append(broker)
    self.clients.extend(broker.clients)

  def create_account(self, broker: "Broker", client: "Client", cash: float):
    account = Account(self, broker, client, broker.type, cash)
    self.accounts.append(account)
    broker.add_account(account)
    client.give_account(account)

  def add_feed(self, feed: "Feed"):
    self.feed = feed
    self.last_day = feed._data[0].dataframe.index[-1]
    print((self.last_day))
  
  def broker_logic(self):
    for broker in self.brokers:
      broker.next()
  
  def client_logic(self):
    for client in self.clients:
      client.next()

  def agent_logic(self):
    self.broker_logic()
    self.client_logic()
    self.broker_logic()
  
  def pre_run(self):
    self.feed.indice = self.feed.index[0]
    # Connect clients to MisterMarket
    for broker in self.brokers:
      self.clients.extend(broker.clients)
      broker.data()
    # Get everyone on the same page
    for client in self.clients:
      client.feed = self.feed
      client.data()

  def run(self):
    self.pre_run()
    for _ in self.feed:
      self.agent_logic()
    
    #for data in self.feed:
    #  self.data_thing(data)
