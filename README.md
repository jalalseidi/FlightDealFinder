# Flight Deals Finder

## 📌 Project Overview
The **Flight Deals Finder** is a Python-based application that helps users find the cheapest flights to their desired destinations. It integrates with the **Amadeus API** to fetch flight data and uses **Google Sheets (Sheety API)** to store destination information, including city names, IATA codes, and the lowest available flight prices.

## 🛠 Technologies Used
- **Python** (requests, dotenv, pprint)
- **Amadeus API** (for flight search and IATA code retrieval)
- **Google Sheets API (Sheety)** (to store and update flight data)

## 🚀 Features
- Fetches destination data from a Google Sheet
- Retrieves IATA codes for cities using Amadeus API
- Updates Google Sheets with correct IATA codes
- Searches for the cheapest flights available
- Displays the best flight prices for each destination

## 🏗 Setup & Installation
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/flight-deals-finder.git
cd flight-deals-finder
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a **.env** file in the root directory and add:
```ini
AMADEUS_API_KEY=your_amadeus_api_key
SHEETY_URL=https://api.sheety.co/your_project/flightDeals/prices
```

### 4️⃣ Run the Script
```sh
python main.py
```

## 📌 API References
- **Amadeus API**: [https://developers.amadeus.com](https://developers.amadeus.com)
- **Sheety API**: [https://sheety.co](https://sheety.co)

## 💡 How It Works
1. **Fetch Destination Data**: Loads city names and checks if IATA codes exist.
2. **Retrieve IATA Codes**: If missing, fetches them from Amadeus API.
3. **Update Google Sheets**: Saves the correct IATA codes in Sheety.
4. **Search for Flights**: Queries Amadeus for the cheapest flights.
5. **Display Results**: Shows the lowest flight prices found.

## ❗ Troubleshooting
- **500 Internal Server Error**: Check the Amadeus API status and ensure your API key is correct.
- **Invalid IATA Codes**: Ensure the Sheety data is updated correctly before running flight searches.
- **400 Flight Search Error**: Ensure all destinations have valid 3-letter IATA codes.

## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributing
Feel free to submit issues or pull requests to improve this project!

---
🚀 Happy Coding & Safe Travels!

