from datetime import datetime
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod


class DataObject(ABC):
    def __init__(self, ticker:str, interval:str, **kwargs):
        self.ticker = ticker
        self.interval = interval
        self.data_df = pd.DataFrame()

    @abstractmethod
    def pull_data(self,start_time:datetime,end_time:datetime)->None:
        pass

    def data_as_df(self)->pd.DataFrame:
        DataObject._check_df(self.data_df)
        return self.data_df

    @staticmethod
    def _check_df(test_df:pd.DataFrame)->None:
        if test_df.empty:
            raise ValueError("Dataframe is empty")
        if list(test_df.columns) != ['data'] or len(test_df.columns) != 1:
            raise ValueError("Dataframe columns are not correct")
        if not test_df['data'].dtype == np.float64:
            raise ValueError("Dataframe column data is not float64")
        if not isinstance(test_df.index, pd.DatetimeIndex):
            raise ValueError("Dataframe index column is not datetime")



