from data_manager import DataManager
from flight_search import FlightSearch
import time

data_manager = DataManager()
sheet_data = data_manager.get_data()
flight_search = FlightSearch()

# Check for missing IATA codes
if sheet_data:
    for row in sheet_data:
        if row["iataCode"] == "TESTING" or not row["iataCode"]:  # Fix condition
            print(f"🚀 Updating IATA code for {row['city']}...")
            row["iataCode"] = flight_search.get_iata_code(row["city"])

            # ✅ Update Google Sheet
            data_manager.update_data(row["id"], {"iataCode": row["iataCode"]})

            time.sleep(1.5)  # ✅ Prevent API rate limiting

print("✅ IATA codes updated in Sheety!")
