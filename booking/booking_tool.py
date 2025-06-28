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
    
    def get_all_bookings(self) -> List[str]:
        """Get all the bookings"""
        bookings = self._sheet.read_all()
        booking_dict_list = [asdict(item) for item in bookings]
        return json.dumps(booking_dict_list, indent=2)
    