import os
import sys
import argparse
import requests
from datetime import datetime

JPL_SIM_URL = "https://space.jpl.nasa.gov/"

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

def simulate_view(source, fov=None, pct=None):
    if not os.path.exists(source):
        print(f"Specified dataset '{source}' not found")
        sys.exit(1)

    output_path = f"{os.path.splitext(source)[0]}_Simulated.jpg"

    image_time = datetime.fromtimestamp(os.path.getmtime(source))
    target = input("Enter the target (e.g., CASSINI, SUN, EARTH, MOON): ").upper()

    default_fov = 1
    camera = "ISSNA" if "ISSNA" in source else "ISSWA"
    if camera == "ISSNA":
        default_fov = 0.35
    elif camera == "ISSWA":
        default_fov = 3.5

    if fov is None or fov < 1 or fov > 90:
        fov = default_fov

    if pct is None or pct < 1 or pct > 100:
        pct = 30

    if target not in TARGET_IDS:
        print(f"Target '{target}' is not supported by the simulator at this time")
        sys.exit(1)

    params = {
        "tbody": TARGET_IDS[target],
        "vbody": TARGET_IDS["CASSINI"],
        "year": image_time.year,
        "month": image_time.month,
        "day": image_time.day,
        "hour": image_time.hour,
        "minute": image_time.minute,
        "rfov": fov,
        "fovmul": 1,
        "bfov": pct,
        "porbs": 1,
        "showac": 1
    }

    r = requests.get(JPL_SIM_URL, params=params)
    if r.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(r.content)
        print("Completed:", output_path)
    else:
        print("Simulation Failed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="Source dataset to model", required=True, type=str)
    parser.add_argument("-f", "--fov", help="Field of view (angle)", required=False, type=float)
    parser.add_argument("-p", "--pct", help="Body width as percentage of image", required=False, type=float)
    args = parser.parse_args()

    simulate_view(args.data, args.fov, args.pct)
