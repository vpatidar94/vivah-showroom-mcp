from datetime import datetime
from typing import List, Optional

from booking_enum.amount_status_enum import AmountStatusEnum
from booking_enum.booking_status_enum import BookingStatusEnum
from dataclass.booking_record import BookingRecord
from util.google_sheet.google_sheet_client import GoogleSheetClient

class GoogleSheetService:
    HEADERS = [
        "id",
        "booking_date",
        "product_code",
        "product_name",
        "booking_status",
        "start_date",
        "end_date",
        "amount",
        "amount_status",
        "is_active"
    ]

    def __init__(self, auth: GoogleSheetClient, spreadsheet_name: str, worksheet_name: str = "Sheet1"):
        self.client = auth.get_client()
        self.sheet = self.client.open(spreadsheet_name).worksheet(worksheet_name)
        self._ensure_headers()

    def _ensure_headers(self):
        current_headers = self.sheet.row_values(1)
        if current_headers != self.HEADERS:
            self.sheet.update('A1', [self.HEADERS])

    def create_row(self, record: BookingRecord) -> str:
        if not record.id:
            record.id = self._generate_next_id()

        if not record.booking_date:
            record.booking_date = datetime.now().strftime("%Y-%m-%d")

        # Validate required fields explicitly
        if not record.product_code:
            raise ValueError("Field 'product_code' is required.")
        if not record.product_name:
            raise ValueError("Field 'product_name' is required.")
        if record.booking_status is None:
            raise ValueError("Field 'booking_status' is required.")

        # Fill defaults for optional fields if None
        record.start_date = record.start_date or None
        record.end_date = record.end_date or None
        record.amount = record.amount or None
        record.amount_status = record.amount_status or AmountStatusEnum.UNPAID.value
        record.is_active = record.is_active or "true"

        row = [
            record.id,
            record.booking_date,
            record.product_code,
            record.product_name,
            record.booking_status,
            record.start_date,
            record.end_date,
            record.amount,
            record.amount_status,
            record.is_active,
        ]

        self.sheet.append_row(row)
        return record.id


    def read_all(self, include_deleted: bool = False) -> List[dict[str, any]]:
        all_values = self.sheet.get_all_values()
        records_data = all_values[1:]
        records = []
        for row in records_data:
            if len(row) < len(self.HEADERS):
                row.extend([""] * (len(self.HEADERS) - len(row)))
            record = BookingRecord(
                id=row[0],
                booking_date=row[1],
                product_code=row[2],
                product_name=row[3],
                booking_status=row[4],
                start_date=row[5],
                end_date=row[6],
                amount=row[7],
                amount_status=row[8],
                is_active=row[9]
            )
            if include_deleted or record.is_active.lower() == "true":
                records.append(record)
        return records


    def read_row(self, row_number: int) -> BookingRecord:
        row = self.sheet.row_values(row_number)
        if len(row) < len(self.HEADERS):
            row.extend([""] * (len(self.HEADERS) - len(row)))
        return BookingRecord(
            id=row[0],
            booking_date=row[1],
            product_code=row[2],
            product_name=row[3],
            booking_status=row[4],
            start_date=row[5],
            end_date=row[6],
            amount=row[7],
            amount_status=row[8],
            is_active=row[9]
        )

    def get_row_by_id(self, record_id: str) -> Optional[BookingRecord]:
        """
        Fetch a row by the given booking ID (e.g., 'VS001').
        Returns a BookingRecord object or None if not found.
        """
        all_rows = self.sheet.get_all_values()

        headers = all_rows[0]
        id_index = headers.index("id")

        for row in all_rows[1:]:
            if len(row) > id_index and row[id_index] == record_id:
                row_data = dict(zip(headers, row))

                # Parse enums and bools properly
                return BookingRecord(
                    id=row_data.get("id"),
                    product_code=row_data.get("product_code") or None,
                    product_name=row_data.get("product_name") or None,
                    booking_status=BookingStatusEnum(row_data["booking_status"]) if row_data.get("booking_status") else None,
                    booking_date=row_data.get("booking_date") or None,
                    start_date=row_data.get("start_date") or None,
                    end_date=row_data.get("end_date") or None,
                    amount=row_data.get("amount") or None,
                    amount_status=AmountStatusEnum(row_data["amount_status"]) if row_data.get("amount_status") else None,
                    is_active=row_data.get("is_active", "True").lower() == "true"
                )

        return None

    
    def find_row_by_id(self, record_id: str) -> int:
        column = self.sheet.col_values(1)
        for index, value in enumerate(column, start=1):
            if value == record_id:
                return index
        raise ValueError(f"Record with ID {record_id} not found.")

    def update_row_by_id(self, record: BookingRecord) -> None:
        row_number = self.find_row_number_by_id(record.id)
        row = [
            str(record.id),
            record.booking_date,
            record.product_code,
            record.product_name,
            record.booking_status,
            record.start_date,
            record.end_date,
            record.amount,
            record.amount_status,
            record.is_active
        ]
        for idx, value in enumerate(row, start=1):
            self.sheet.update_cell(row_number, idx, value)

    def delete_row_by_id(self, record_id: str) -> None:
        row_number = self.find_row_number_by_id(record_id)
        self.sheet.update_cell(row_number, self.HEADERS.index("is_active") + 1, "false")
    
    def find_row_number_by_id(self, record_id: str) -> int:
        """
        Returns the 1-based row number for the given booking ID.
        """
        column = self.sheet.col_values(1)  # column A = id column
        for i, cell in enumerate(column, start=1):
            if cell == record_id:
                return i
        raise ValueError(f"Booking with ID {record_id} not found.")
        
    def _generate_next_id(self) -> str:
        existing_ids = self.sheet.col_values(1)[1:]  # skip header
        max_num = 0

        for vs_id in existing_ids:
            if vs_id.startswith("VS"):
                try:
                    num = int(vs_id[2:])
                    max_num = max(max_num, num)
                except ValueError:
                    continue

        next_id = max_num + 1
        return f"VS{next_id:03d}"  # e.g., VS001
    
