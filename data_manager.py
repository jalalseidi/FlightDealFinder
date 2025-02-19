import requests

import flight_search
from flight_search import FlightSearch

SHEETY_URL = "https://api.sheety.co/a1776bed53430a67045c94021b85d79f/flightDeals/prices"

class DataManager:
    def __init__(self):
        self.sheety_url = SHEETY_URL
        self.data = []

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_URL)
        data = response.json()
        self.destination_data = data["prices"]
        # Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # pprint(data)
        return self.destination_data

        # In the DataManager Class make a PUT request and use the row id from sheet_data
        # to update the Google Sheet with the IATA codes. (Do this using code).

    def update_destination_codes(self):
        flight_search_instance = FlightSearch()
        for city in self.destination_data:
            if city["iataCode"] == "ERROR" or city["iataCode"] == "" or city["iataCode"] == "N/A":
                print(f"Updating IATA code for {city['city']}...")  # Debugging
                new_code = flight_search_instance.get_destination_code(city["city"])
                city["iataCode"] = new_code  # Update the local data

                new_data = {
                    "price": {
                        "iataCode": new_code
                    }
                }
                response = requests.put(
                    url=f"{SHEETY_URL}/{city['id']}",
                    json=new_data
                )
                print(f"Updated {city['city']} with IATA code {new_code}. Response: {response.text}")



