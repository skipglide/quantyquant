from typing import Any

import pandas as pd


class RelativeRow:
  
  def __init__(self, dataframe: pd.DataFrame):
    self.dataframe = dataframe
    self.index = 0
    self.k = len(dataframe) - 1
    
  def set_index(self, index: int):
    self.index = index
  
  def __getitem__(self, relative_index: int):
    future_bound = self.k - self.index
    past_bound = future_bound - self.k
    if relative_index < past_bound or relative_index > future_bound:
      dict_data = {'Open': None,
                   'High': None,
                   'Low': None,
                   'Close': None}
      return pd.Series(dict_data)
    indice = self.index + relative_index
    return self.dataframe.iloc[indice]

class Data:
  
  def __init__(self, dataframe: pd.DataFrame):
    self.dataframe = dataframe
    self._index = 0
    self._relative_row = RelativeRow(dataframe)
  
  def __len__(self) -> int:
      return len(self.dataframe)

  def __getitem__(self, index: int):
    self._relative_row.set_index(self._index)
    return self._relative_row[index] #self.dataframe.iloc[index]
    
  def __iter__(self):
    self._index = 0  # Reset the iteration index
    return self
  
  def __next__(self):
    if self._index >= len(self.dataframe):
      raise StopIteration
    self._relative_row.set_index(self._index)
    self._index += 1
    return self._relative_row

  def set_index(self, index: int):
    self._index = index


class Feed:

  def __init__(self):
    self._data = []
    self.tickers = []
    self.indice: Any # The current indice of all the Data in _data
    self.index = []


  def __iter__(self):
    self._index = 0  # Reset the iteration index
    self.indice = self.index[0]
    return self

  def __next__(self):
    if self._index >= len(self.index):
      raise StopIteration
    result = [data.set_index(self._index) for data in self._data]
    self._index += 1
    self.indice = self.index[self._index - 1]
    return result

  def __getitem__(self, index):
    if isinstance(index, int):
      return self._data[index]
    elif isinstance(index, str):
      return self._data[self.tickers.index(index)]
    else:
      raise TypeError(f"Invalid index type {type(index)}")
