from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional

class BaseDataProvider(ABC):
    @abstractmethod
    def fetch_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        pass