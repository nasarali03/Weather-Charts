import pandas as pd

def read_data(timestamp):
    try:
        data_file = f"Decoded_Data/{timestamp}.csv"
        data = pd.read_csv(data_file)

        # Filter out stations with elevation > 800 meters
        filtered_data = data[data["Elevation"] <= 800]

        return filtered_data
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", str(e))


read_data("2025021100")
print()