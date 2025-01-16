import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

# Load the dataset
data = pd.read_csv('analyses.csv', delimiter=';')

# Convert time columns to datetime
data['Open'] = pd.to_datetime(data['Open'])
data['Close'] = pd.to_datetime(data['Close'])

# Extract useful time features from 'Open'
data['Hour'] = data['Open'].dt.hour
data['DayOfWeek'] = data['Open'].dt.dayofweek
data['TradeDuration'] = (data['Close'] - data['Open']).dt.total_seconds()

# Filter and preprocess the data
features = ['Hour', 'DayOfWeek', 'TradeDuration', 'Volume', 'Symbol']
label = 'Profit'

# Encode categorical data (e.g., 'Symbol')
label_encoder = LabelEncoder()
data['SymbolEncoded'] = label_encoder.fit_transform(data['Symbol'])

# Prepare the feature matrix (X) and target vector (y)
X = data[['Hour', 'DayOfWeek', 'TradeDuration', 'Volume', 'SymbolEncoded']]
y = data['Profit']

# Adjust weight for profit in the learning process
# Here, we scale 'Profit' more significantly during training
profit_weight = 2  # Higher weight for profit
weighted_y = y * profit_weight

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, weighted_y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Model RMSE: {rmse}")

# Suggest the best entry time and volume for each asset
optimal_suggestions = {}
for symbol in data['Symbol'].unique():
    symbol_data = data[data['Symbol'] == symbol]
    best_combination = None
    best_profit = -np.inf

    # Use only hours present in the dataset for this symbol
    unique_hours = symbol_data['Hour'].unique()

    for hour in unique_hours:
        for volume in np.linspace(symbol_data['Volume'].min(), symbol_data['Volume'].max(), num=10):
            test_data = pd.DataFrame({
                'Hour': [hour],
                'DayOfWeek': [symbol_data['DayOfWeek'].mode()[0]],
                'TradeDuration': [symbol_data['TradeDuration'].mean()],
                'Volume': [volume],
                'SymbolEncoded': [label_encoder.transform([symbol])[0]]
            })
            predicted_profit = model.predict(test_data)[0] / profit_weight

            if predicted_profit > best_profit:
                best_combination = {'Hour': hour, 'Volume': volume}
                best_profit = predicted_profit

    optimal_suggestions[symbol] = {
        'BestHour': best_combination['Hour'] if best_combination else symbol_data['Hour'].mode()[0],
        'BestVolume': best_combination['Volume'] if best_combination else symbol_data['Volume'].mean(),
        'PredictedProfit': best_profit
    }

# Display the results
for asset, info in optimal_suggestions.items():
    print(f"Asset: {asset}, Best Entry Hour: {info['BestHour']}, Best Volume: {info['BestVolume']:.2f}, Predicted Profit: {info['PredictedProfit']:.2f}")
