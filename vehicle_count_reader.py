import pandas as pd

def read_latest_vehicle_count(filename):
    df = pd.read_csv(filename, header = None)
    latest_row = df.iloc[-1]  # Get the last row of the DataFrame
    latest_vehicle_count = latest_row[1]  # Assuming the column name is 'vehicle_count'
    return latest_vehicle_count

# print(read_latest_vehicle_count("vehicle_log.csv"))