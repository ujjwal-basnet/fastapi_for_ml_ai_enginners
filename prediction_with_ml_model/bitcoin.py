from datetime import timedelta
import pandas as pd
import pickle

def predict_future_close(user_date_str):
    
    #Load preprocessed DataFrame
    sorted_df = pd.read_pickle("prediction_with_ml_model/processed_df.pkl")

# Load trained model
    with open("prediction_with_ml_model/bitcoin_model.pkl", "rb") as f:
        model = pickle.load(f)

    future_df = sorted_df.copy()
    target_date = pd.to_datetime(user_date_str)

    last_known_date = pd.Timestamp.fromordinal(int(future_df['Date'].iloc[-1]))

    while last_known_date < target_date:
        lag1 = future_df.iloc[-1]['Close']
        lag2 = future_df.iloc[-2]['Close']
        lag3 = future_df.iloc[-3]['Close']
        ma3 = (lag1 + lag2 + lag3) / 3

        next_date = last_known_date + timedelta(days=1)
        next_date_ordinal = next_date.toordinal()

        # Use DataFrame to match feature names
        X_pred = pd.DataFrame([[next_date_ordinal, lag1, lag2, lag3, ma3]],
                              columns=['Date', 'Close_lag1', 'Close_lag2', 'Close_lag3', 'MA3'])

        predicted_close = model.predict(X_pred)[0]

        # Append row using concat
        new_row = pd.DataFrame({'Date': [next_date_ordinal], 'Close': [predicted_close]})
        future_df = pd.concat([future_df, new_row], ignore_index=True)

        last_known_date = next_date

    return predicted_close


# Only runs when executing this file directly (eg from  .. import wont print this)
if __name__ == "__main__":
    test_date = "2026-01-05"
    predicted = predict_future_close(test_date)
    print(f"Predicted Close for {test_date}: {predicted}")