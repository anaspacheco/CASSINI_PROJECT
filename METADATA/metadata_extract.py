import requests
import pandas as pd
from astropy.table import Table
import csv
import io

#Label URL
label_url = 'https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/coiss_2052/index/index.lbl'

#Data URL
data_url = 'https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/coiss_2052/index/index.tab'

# Fetching the label file
label_response = requests.get(label_url)
label_response.raise_for_status()  # Check if the request was successful
label = label_response.text


#Assign specific VOLUME ID (can automate this later on)
volume_id = "coiss_2052"

# Extracting column names from the label file
column_names = []
lbl_lines = label.split('\n')
name_counts = {}
column_name = None

for line in lbl_lines:
    if 'NAME' in line:
        column_name = line.split("=")[1].strip()
        if not column_name:
            print("Unable to extract column names from the LBL file.")
            exit(1)
        name_counts[column_name] = 1
        column_names.append(column_name)
    if 'ITEMS' in line:
        number_items = line.split("=")[1].strip()
        number_items = int(number_items)
        for i in range(number_items - 1):
            name_counts[column_name] = name_counts.get(column_name, 0) + 1
            new_column_name = f"{column_name}_{name_counts[column_name]}"
            column_names.append(new_column_name)
        column_name = None
    

# Fetching the data file
data_response = requests.get(data_url)
data_response.raise_for_status()  # Check if the request was successful
data = data_response.text

# Reading data using pandas
df = pd.read_csv(io.StringIO(data), delimiter=',', header=None, names=column_names)

# Converting to Astropy table
t = Table.from_pandas(df)

# Save as CSV
t.write(volume_id+'.csv', format='csv', overwrite=True)

print("CSV file successfully created.")
