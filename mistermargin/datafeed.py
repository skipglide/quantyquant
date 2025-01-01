import pandas as pd

from ._data import Data, Feed


class YahooFinanceCSVData(Feed):

  def __init__(self):
    super().__init__()

  def read_data(self,
                file_path: str,
                ticker_symbol: str,
                start_date: str = '',
                end_date: str = ''):
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    if not start_date:
      start_date = df.index[0].date().strftime('%Y-%m-%d')
    if not end_date:
      end_date = df.index[-1].date().strftime('%Y-%m-%d')
    df['Adj Factor'] = df['Adj Close'] / df['Close']
    df['Open'] = df['Open'] * df['Adj Factor']
    df['High'] = df['High'] * df['Adj Factor']
    df['Low'] = df['Low'] * df['Adj Factor']
    df['Close'] = df['Close'] * df['Adj Factor']
    df.drop(columns=['Adj Close','Adj Factor'], inplace=True)

    data = Data(df.loc[start_date:end_date])

    if not self.index:
      self.index = df.loc[start_date:end_date].index.to_list()
    self._data.append(data)
    self.tickers.append(ticker_symbol)
