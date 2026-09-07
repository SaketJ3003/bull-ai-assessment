from typing import Optional

from pydantic import BaseModel


class TestFinancialData(BaseModel):
    company_name: Optional[str] = None
    rating: Optional[str] = None
    target_price: Optional[float] = None
    current_price: Optional[float] = None