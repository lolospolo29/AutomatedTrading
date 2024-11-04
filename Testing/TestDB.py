from pymongo import MongoClient

# Connect to MongoDB instance
client = MongoClient('mongodb://127.0.0.1:27017')

# Access the 'TradingViewData' database
db = client.TradingViewData

# Access the 'Data' collection
collection = db.currentData

# Insert a sample document into the 'Data' collection
document = {
        "tradingViewData": {
            "ticker": "BTC",
            "Broker": "Bybit",
            "Strategy": "FVG",
            "close": 175.30,
            "open": 172.40,
            "high": 176.00,
            "low": 170.50,
            "strategie": {
                "name": "MovingAverage",
                "parameters": {
                    "short_term_period": 5,
                    "long_term_period": 20,
                    "buy_signal": True,
                    "sell_signal": False
                },
                "additional_info": [
                    {
                        "date": "2024-09-01",
                        "signal": "buy"
                    },
                    {
                        "date": "2024-09-02",
                        "signal": "hold"
                    }
                ]
            }}
}

# Insert the document into the collection
result = collection.insert_one(document)

# Print the inserted document's ID
print("Inserted document ID:", result.inserted_id)


# Ein einzelnes Dokument abrufen
document = collection.find_one({"symbol": "TSLA"})  # Hier z.B. ein Dokument mit dem Symbol "TSLA"
print("Einzelnes Dokument:", document)

# Mehrere Dokumente abrufen
documents = collection.find()  # Gibt alle Dokumente in der Collection zurück

# Durch alle Dokumente iterieren und sie ausgeben
for doc in documents:
    print(doc)

# Close the connection
client.close()
