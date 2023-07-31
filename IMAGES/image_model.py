import requests
from bs4 import BeautifulSoup
import os
import sys
import argparse
import rasterio
import pvl
from datetime import datetime
import contextlib

'''
Much of this code was borrowed from: https://github.com/kmgill/cassini_processing/blob/master/getmodel.py
Several changes were done in order to avoid the use of the ISIS3 Software
Also, LBL file is now sourced from its HTML, so that image does not have to be downloaded
'''

#Adding comment 


#Label for the image (with metadata), provide this manually please
#Can also automate this later on if a large scale processing is needed 

label_url = 'https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/coiss_2052/data/1609475102_1609640902/W1609475157_1.LBL'

#Image ID
image_id = os.path.splitext(os.path.basename(label_url))[0]

# Fetching the label file
label_response = requests.get(label_url)
label_response.raise_for_status()  
label_content = label_response.content.decode("utf-8")  


#Loading the label file using pvl
try:
    label_data = pvl.loads(label_content)
except FileNotFoundError:
    print("Error: The specified label file does not exist.")

image_number = label_data['IMAGE_NUMBER']

image_time= label_data['IMAGE_TIME']

camera = label_data['INSTRUMENT_ID']

target = label_data['TARGET_NAME']

# Extract individual date and time components
day = image_time.day
month = image_time.strftime("%B")
month_number = datetime.strptime(month, "%B").month
year = image_time.year
hour = image_time.hour
minute = image_time.minute
second = image_time.second

# URL of website
URL = "https://space.jpl.nasa.gov/cgi-bin/wspace/"

session = requests.Session()

with contextlib.redirect_stdout(None):
    response = session.get(URL)

with contextlib.redirect_stdout(None):
    soup = BeautifulSoup(response.content, "html.parser")

#Target IDS
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
parser.add_argument("-f", "--fov", help="Field of view (angle)", required=False, type=float)
parser.add_argument("-p", "--pct", help="Body width as percentage of image", required=False, type=float)

use_fov = True

args = parser.parse_args()

fov = args.fov
pct = args.pct

output_path = f"{image_id}_Simulated.jpg"

default_fov = 1
if camera == "ISSNA":
    default_fov = 45
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
        "month": month_number,
        "day": day,
        "year": year,
        "hour": hour,
        "minute": minute,
        "fovmul": 1 if use_fov else -1,
        "rfov": fov,
        "bfov": pct,
        "showac": 1,
    }

complete_url = f"{URL}?tbody={TARGET_IDS[target]}&vbody={TARGET_IDS['CASSINI']}&month={month_number}&day={day}&year={year}&hour={hour}&minute={minute}&fovmul={1 if use_fov else -1}&rfov={fov}&bfov={pct}&showac=1"

with contextlib.redirect_stdout(None):
    r = session.get(complete_url)

if r.status_code == 200:
    with open(output_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)
    print ("Completed:", output_path)
else:
    print ("Simulation Failed")
