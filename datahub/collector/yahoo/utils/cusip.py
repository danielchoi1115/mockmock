import pandas as pd
from pandas import DataFrame
def get_cusip_all() -> DataFrame:
    return pd.read_csv('/home/sychoi/mockmock/datahub/collector/yahoo/utils/cusip_ticker.csv', sep="|")
    

