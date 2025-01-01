from ._document import Document


class Account(Document):
  """
  An account is managed by a Broker and owned by a client.
  It either is or isn't a margin account and has a cash balance.
  """

  def __init__(self, market: "Market", broker: "Broker", client: "Client", type: str, cash: float):
    super().__init__()
    self.market = market
    self.broker = broker
    self.client = client
    self.type = type
    self.cash = cash
    self.open_orders = []
    self.closed_orders = []
    self.canceled_orders = []
    self.trade_history = []
    self.securities = set()
    self.positions = []

  def rules(self):
    pass

  def add_order(self, order: "Order"):
    self.open_orders.append(order)

  @property
  def account_value(self):
    return sum([position.size * self.market.feed[position.security][0]['Close'] for position in self.positions]) + self.cash
  
  def add_security(self, security: str):
    self.securities.add(security)
  
  def generate_report(self):
    pass