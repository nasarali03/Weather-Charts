import os
import requests
from controllers import store_synop_data

def download_file(timestamp):

    url = f"http://www.pmdnmcc.net/websites/RealTime/Data/{timestamp}syn.txt"

    directory = "Synop"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, f"{timestamp}syn.txt")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, 'wb') as    file:
            file.write(response.content)
        print(f"File saved as {filename}")
        store_synop_data(filename)
        return True
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return False
a=["00","03","06","09","12","15","18","21"]
b=['01','02','03','04','05','06','07','08','09','10','11']
for x in b:
    for y in a:
        download_file(f"202502{x}{y}")
# for x in a:
#     download_file(f"20250203{x}")

