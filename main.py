
from fastmcp import FastMCP
from booking.booking_tool import BookingTool
from util.google_sheet.google_sheet_client import GoogleSheetClient
from util.google_sheet.google_sheet_service import BookingRecord, GoogleSheetService

def main():
    mcp = FastMCP("vivah_showroom_mcp")
    
    bookingTool = BookingTool(mcp)
    bookingTool.init_tools()
    mcp.run(transport="streamable-http" )
    
    
    # auth = GoogleSheetClient()
    # sheet = GoogleSheetService(auth, spreadsheet_name="Vivah Showroom DB", worksheet_name="Booking")

    # sheet.create_row(BookingRecord(
    #     product_code= "P123",
    #     product_name= "Lehnga",
    #     start_date= "2025-07-22",
    #     end_date= "2025-07-24",
    #     amount= "500",
    #     booking_status="CONFIRMED"
    # ))
    # print(sheet.get_all_bookings())



if __name__ == "__main__":
    print("Starting Vivah Showroom MCP Server...")
    main()
