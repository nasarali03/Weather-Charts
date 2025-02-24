import os
import requests

def download_file(timestamp):
    # Detect if running on Railway (Railway sets `RAILWAY_ENVIRONMENT` variable)
    if "RAILWAY_ENVIRONMENT" in os.environ:
        BASE_DIR = "/app/data/"  # Railway persistent storage
    else:
        BASE_DIR = os.path.join(os.getcwd(), "data")  # Local storage

    synop_dir = os.path.join(BASE_DIR, "Synop")

    # Ensure the directory exists
    os.makedirs(synop_dir, exist_ok=True)

    # File path
    filename = os.path.join(synop_dir, f"{timestamp}syn.txt")

    # URL of the file to download
    url = f"http://www.pmdnmcc.net/websites/RealTime/Data/{timestamp}syn.txt"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"File saved as {filename}")
        return True
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return False


# a=["00","03","06","09","12","15","18","21"]
# b=['07','08','09','10','11','12','13','14','15','16','17']
# for x in b:
#     for y in a:
#         download_file(f"202502{x}{y}")
# for x in a:
download_file(f"2025022400")

