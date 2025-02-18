import requests
import os
from datetime import datetime, timedelta
from flight_data import FlightData


IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
FLIGHT_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
ORIGIN_CITY_IATA = "LON"  # London
CURRENCY = "GBP"


class FlightSearch:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.api_secret = os.environ.get("API_SECRET")
        self.token = self._get_new_token()


    def _get_new_token(self):
        """Fetch a new API token from Amadeus and handle missing credentials."""
        if not self.api_key or not self.api_secret:
            print("❌ API credentials are missing. Check your environment variables.")
            return None

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }

        response = requests.post(url=TOKEN_URL, headers=headers, data=body)

        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data.get("access_token")
            self.token_expires = datetime.now() + timedelta(seconds=token_data.get("expires_in", 3600))
            return self.token
        else:
            print(f"❌ Error fetching token: {response.status_code}, {response.text}")
            return None


    def get_iata_code(self, city_name):
        """Gets the IATA code for a given city using Amadeus API."""
        if not self.token:
            print("❌ No API token. Cannot fetch IATA code.")
            return "ERROR"

        print(f"🔍 Fetching IATA code for {city_name}...")
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"keyword": city_name, "max": 1}

        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=params)

        if response.status_code == 200:
            try:
                code = response.json()["data"][0]["iataCode"]
                print(f"✅ IATA Code for {city_name}: {code}")
                return code
            except (IndexError, KeyError):
                print(f"⚠️ No IATA code found for {city_name}.")
                return "N/A"
        else:
            print(f"❌ API Request Failed: {response.status_code}, {response.text}")
            return "ERROR"

    def find_cheapest_flight(self, destination_iata):
        """Finds the cheapest non-stop round-trip flight to a given destination."""
        if not self.token:
            print("❌ No API token. Cannot search for flights.")
            return FlightData(price="N/A", origin_airport="N/A", destination_airport="N/A",
                              out_date="N/A", return_date="N/A")

        # Set up date range (tomorrow to 6 months later)
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        six_months_later = (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")

        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "originLocationCode": ORIGIN_CITY_IATA,
            "destinationLocationCode": destination_iata,
            "departureDate": tomorrow,
            "returnDate": six_months_later,
            "adults": 1,
            "nonStop": True,
            "currencyCode": CURRENCY,
            "max": 1  # Get only the cheapest option
        }

        response = requests.get(url=FLIGHT_SEARCH_URL, headers=headers, params=params)

        if response.status_code == 200:
            try:
                data = response.json()["data"][0]  # Get first (cheapest) flight
                price = data["price"]["total"]
                departure_airport = data["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                arrival_airport = data["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
                out_date = data["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
                return_date = data["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")[0]

                return FlightData(price=price, origin_airport=departure_airport,
                                  destination_airport=arrival_airport,
                                  out_date=out_date, return_date=return_date)
            except (IndexError, KeyError):
                print(f"⚠️ No flights found for {destination_iata}.")
                return FlightData(price="N/A", origin_airport="N/A", destination_airport="N/A",
                                  out_date="N/A", return_date="N/A")
        else:
            print(f"❌ API Error: {response.status_code}, {response.text}")
            return FlightData(price="N/A", origin_airport="N/A", destination_airport="N/A",
                              out_date="N/A", return_date="N/A")
