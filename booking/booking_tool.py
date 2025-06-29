from dataclasses import asdict
import json
from typing import List
from mcp.server.fastmcp import FastMCP

from dataclass.booking_record import BookingRecord
from util.google_sheet.google_sheet_client import GoogleSheetClient
from util.google_sheet.google_sheet_service import GoogleSheetService

class BookingTool:
    def __init__(self, mcp: FastMCP):
        auth = GoogleSheetClient()
        self._sheet = GoogleSheetService(auth, spreadsheet_name="Vivah Showroom DB", worksheet_name="Booking")
        self._mcp = mcp
    
    def init_tools(self):
        self._mcp.tool(self.get_all_bookings)
        self._mcp.tool(self.get_booking_by_id)
        self._mcp.tool(self.create_booking)
        self._mcp.tool(self.delete_booking_by_id)
    
    def get_all_bookings(self) -> List[str]:
        """Get all the bookings"""
        bookings = self._sheet.read_all()
        booking_dict_list = [asdict(item) for item in bookings]
        return json.dumps(booking_dict_list, indent=2)
    
    def get_booking_by_id(self, id: str) -> str:
        """Get booking by id"""
        bookings = self._sheet.get_row_by_id(id)
        return json.dumps(asdict(bookings), indent=2)
    
    def create_booking(self, booking: BookingRecord) -> str:
        """Get booking by id"""
        id = self._sheet.create_row(booking)
        return id
    
    def delete_booking_by_id(self, id: str) -> str:
        """Delete booking by id"""
        self._sheet.delete_row_by_id(id)
    