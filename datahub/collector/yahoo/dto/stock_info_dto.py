from pydantic import BaseModel
from typing import Dict, Literal

class StockInfo(BaseModel):
    ticker: str
    cusip: str
    longName: str
    quoteType: str
    currency: str
    exchangeTimezoneName: str
    fullExchangeName: str
    sector: str
    industry: str
    ...