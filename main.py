from python.download_synop import download_file
from python.decoding import process_synop_files
from python.contours import generate_geojson
from datetime import datetime, timedelta, timezone
from python.delete import delete_file
import time,os,sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "python")))
# print(sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "python"))))

def main():
    now = datetime.now(timezone.utc)
    hour = now.hour
    print(hour)
    interval_start_hour = (hour // 3) * 3
    timestamp = now.replace(hour=interval_start_hour, minute=0, second=0, microsecond=0).strftime("%Y%m%d%H")
    if str(hour) == "00":
        delete_file("Decoded_Data")
        delete_file("contours_data")
        delete_file("Synop")

    if "RAILWAY_ENVIRONMENT" in os.environ:
        BASE_DIR = "/app/data/"  # Railway persistent storage
    else:
        BASE_DIR = os.path.join(os.getcwd(), "data")  # Local storage

    # Define the directory for GeoJSON files
    contours_dir = os.path.join(BASE_DIR, "contours_data")

    # Ensure the directory exists
    os.makedirs(contours_dir, exist_ok=True)

    # Set the JSON file path
    json_file_path = os.path.join(contours_dir, f"{timestamp}.geojson")
    if os.path.exists(json_file_path):
        print("Data already downloaded")
        download_success = False
    else:
        print("Running download_synop...")
        download_success = download_file(timestamp)

    if download_success:
        print("Decoding...")
        station_codes_file = "static/WMO_stations_data.csv"
        if "RAILWAY_ENVIRONMENT" in os.environ:
            BASE_DIR = "/app/data/"  # Railway persistent storage
        else:
            BASE_DIR = os.path.join(os.getcwd(), "data")  # Local storage

        station_codes_file = "static/WMO_stations_data.csv"
        directory = os.path.join(BASE_DIR, "Synop")
        output_directory = os.path.join(BASE_DIR, "Decoded_Data")
        process_synop_files(station_codes_file, directory, output_directory, timestamp)
        
        # Wait for some time to ensure data is saved
        time.sleep(25)
        
        print("Generating Contours...")
        generate_geojson(timestamp)
    
def schedule_task():
    while True:
        now = datetime.now(timezone.utc)
        print(f"Current time: {now}")

        # Run the main task
        main()
        # Calculate the time until the next hour
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        time_until_next_hour = (next_hour - now).total_seconds()
        
        time_until_next_hour_minutes = int(time_until_next_hour / 60)
        
        print(f"Sleeping for {time_until_next_hour_minutes} minutes until next hour.")
        time.sleep(time_until_next_hour)

if __name__ == "__main__":
    schedule_task()
