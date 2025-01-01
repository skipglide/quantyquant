from dateutil.relativedelta import relativedelta

from mistermargin import Broker, Client, MisterMarket, YahooFinanceCSVData

feed = YahooFinanceCSVData()
# File path to the Yahoo Finance CSV data
file_path = 'QQQ.csv'
start_date='2024-01-01'
end_date='2023-12-31'
feed.read_data(file_path, 'QQQ', start_date=start_date)
feed.read_data('^VIX.csv', 'VIX', start_date=start_date)

# Mister Market is the Market
market = MisterMarket()

# The Market needs data
market.add_feed(feed)

# A broker works as a middleman
broker = Broker()

# A client is someone with their own ideas
class MyClient(Client):

  def __init__(self):
    super().__init__()
  
  def data(self):
    df = feed['QQQ'].dataframe
    df['YearMonth'] = df.index.to_period('M')
    self.buy_schedule = df.groupby('YearMonth',).apply(lambda x: x.index.min(), include_groups=False)
    self.size = self.starting_cash / 12
  
  def next(self):
    todays_date = feed['QQQ'][0].name
    if todays_date in self.buy_schedule.values:
      self.buy('QQQ', self.size)
    for position in self.account.positions:
      if (position.open_date + relativedelta(months=3)) >= todays_date:
        self.sell(position.security, position.size)

# Of how the market behaves
client = MyClient()

# And the broker goes to the market
market.add_broker(broker)

# A client finds a broker.
broker.add_client(client)

market.run()

for account in market.accounts:
  for order in account.open_orders:
    #print((order))
    pass
  for order in account.closed_orders:
    #print((order))
    pass
  for trade in account.trade_history:
    #print((trade))
    pass
  for position in account.positions:
    #print((position))
    pass
  print(account.securities)
  print(f"account_value={account.account_value}")



print("Done")