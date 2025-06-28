from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BookingRecord:
    product_code: str                      # required
    product_name: str                      # required
    booking_status: str                    # required, use BookingStatusEnum

    id: Optional[str] = field(default=None)
    booking_date: Optional[str] = field(default=None)
    start_date: Optional[str] = field(default=None)
    end_date: Optional[str] = field(default=None)
    amount: Optional[str] = field(default=None)
    amount_status: Optional[str] = field(default=None)
    is_active: Optional[str] = field(default="true")