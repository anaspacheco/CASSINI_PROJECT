import requests
from bs4 import BeautifulSoup
import os
import sys
import argparse
import rasterio
import pvl
from datetime import datetime

image_id = "N1610585886_1"
label_file_path ='/Users/anasofiapacheco/Desktop/'+image_id+'.LBL'

# Loading the label file using pvl
try:
    with open(label_file_path, 'r') as f:
        label_data = pvl.load(f)
except FileNotFoundError:
    print("Error: The specified label file does not exist.")

# Extract Image Number
image_number = label_data['IMAGE_NUMBER']

#print("Image Number:", image_number)

# Extract Date and Time Information
image_time= label_data['IMAGE_TIME']

#Extract Instrument_ID:
camera = label_data['INSTRUMENT_ID']

#Extract target name 
target = label_data['TARGET_NAME']

# Extract individual date and time components
day = image_time.day
month = image_time.strftime("%B")
year = image_time.year
hour = image_time.hour
minute = image_time.minute
second = image_time.second

# Define the URL of the JPL NASA website
URL = "https://space.jpl.nasa.gov/"

# Create a session to maintain cookies and headers across requests
session = requests.Session()

# Send a GET request to the website to retrieve the initial page and extract the required form data
response = session.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

TARGET_IDS = {
    "CASSINI": -82,
    "SUN": 1000,
    "EARTH": 399,
    "MOON": 301,
    "JUPITER": 599,
    "IO": 501,
    "EUROPA": 502,
    "GANYMEDE": 503,
    "CALLISTO": 504,
    "SATURN": 699,
    "MIMAS": 601,
    "ENCELADUS": 602,
    "TETHYS": 603,
    "DIONE": 604,
    "RHEA": 605,
    "TITAN": 606,
    "HYPERION": 607,
    "IAPETUS": 608,
    "PHEOBE": 609,
    "PLUTO": 999
}

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data", help="Source dataset to model", required=True, type=str)
parser.add_argument("-f", "--fov", help="Field of view (angle)", required=False, type=float)
parser.add_argument("-p", "--pct", help="Body width as percentage of image", required=False, type=float)

use_fov = True

args = parser.parse_args()

source = args.data
fov = args.fov
pct = args.pct

output_path = f"{image_id}_Simulated.jpg"

default_fov = 1
if camera == "ISSNA":
    default_fov = 0.35
elif camera == "ISSWA":
    default_fov = 3.5

if fov is None or fov < 1 or fov > 90:
     fov = default_fov

if pct is not None:
    use_fov = False
if pct is None or pct < 1 or pct > 100:
    pct = 30

if target not in TARGET_IDS:
    print ("Target '%s' is not supported by the simulator at this time")
    exit(1)

params = {
        "tbody": TARGET_IDS[target],
        "vbody": TARGET_IDS["CASSINI"],
        "year": image_time.year,
        "month": image_time.month,
        "day": image_time.day,
        "hour": image_time.hour,
        "minute": image_time.minute,
        "rfov": fov,
        "fovmul": 1 if use_fov else -1,
        "bfov": pct,
        "porbs": 1,
        "showac": 1,
        "submit": "Run Simulator"
    }

r = requests.get(URL, params=params)
if r.status_code == 200:
    with open(output_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)
    print ("Completed:", output_path)
else:
    print ("Simulation Failed")