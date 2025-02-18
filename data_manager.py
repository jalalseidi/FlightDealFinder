import requests

SHEETY_URL = "https://api.sheety.co/a1776bed53430a67045c94021b85d79f/flightDeals/prices"

class DataManager:
    def __init__(self):
        self.sheety_url = SHEETY_URL
        self.data = []

    def get_data(self):
        """Fetches data from the Google Sheet via Sheety API."""
        response = requests.get(self.sheety_url)
        if response.status_code == 200:
            self.data = response.json().get("prices", [])  # Get "prices" list safely
            return self.data
        else:
            print(f"❌ Error fetching data: {response.status_code}, {response.text}")
            return None

    def update_data(self, row_id, updated_info):
        """Updates a specific row in the Google Sheet using Sheety API."""
        new_data = {"price": updated_info}  # ✅ Ensure correct JSON format for Sheety API

        response = requests.put(
            url=f"{self.sheety_url}/{row_id}",
            json=new_data,
        )

        if response.status_code == 200:
            print(f"✅ Successfully updated row {row_id} with {updated_info}")
        else:
            print(f"❌ Error updating row {row_id}: {response.status_code}, {response.text}")

