from datetime import datetime
import nasdaqdatalink
import pandas as pd
from src.Data.DataObject import DataObject




class PERatio(DataObject):
    def __init__(self, ticker:str = 'PE', interval:str = 'monthly', **kwargs):
        super().__init__(ticker,interval,**kwargs)

    def pull_data(self,start_time:datetime,end_time:datetime):
        self.data_df = nasdaqdatalink.get("MULTPL/SP500_PE_RATIO_MONTH", start_date=start_time, end_date=end_time)
        self._format_data(self.data_df)

    @staticmethod
    def _format_data(format_df)->None:
        format_df.rename(columns={'Value': 'data'}, inplace=True)
        format_df['data'] = format_df['data'].astype(float)


if __name__ == '__main__':
    pe = PERatio()
    pe.pull_data(datetime(2010,1,1),datetime(2020,1,1))
    print(pe.data_as_df())