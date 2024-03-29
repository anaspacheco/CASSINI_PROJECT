#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 18:15:04 2023

@author: mayanesen
"""

# PLOTS OF POSITION VS TIME USING CASSINI METADATA

#%% libraries and packages needed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
import astropy
import requests
from astropy.table import Table
import csv
import io

#%% import the csv from a url

#Label URL
label_url = 'https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/coiss_2052/index/index.lbl'

#Data URL
data_url = 'https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/coiss_2052/index/index.tab'

# Fetching the label file
label_response = requests.get(label_url)
label_response.raise_for_status()  # Check if the request was successful
label = label_response.text


# Assign specific VOLUME ID (can automate this later on)
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

metadata = pd.DataFrame(df).to_numpy()


#%% plotting columns 79 to end using a for loop

time = metadata[:,68] # SPACECRAFT_CLOCK_START_COUNT


for i in range(79, 139):
    if type(metadata[1,i]) != str:
        print(column_names[i], i)
        y = metadata[:,i].reshape(5460,1)
        plt.plot(time, y, "o", markersize=4)
        point_label = metadata[:,73]
        for j, label in enumerate(point_label):
            if str(label) != "SATURN                  ":
                plt.annotate(str(label), (time[j], y[j]), xytext=(5, 5), textcoords="offset points", fontsize=7)
            else:
                plt.plot(time[j], y[j], "o", markersize=4, color='red')
        plt.ylabel(column_names[i] + " (units?)") # need to adjust the units
        plt.xlabel('SPACECRAFT_CLOCK_START_COUNT (s)')
        plt.suptitle(column_names[i] + " vs. SPACECRAFT_CLOCK_START_COUNT")
        plt.title('Volume COISS 2052', fontsize=10)
        L, H = np.percentile(y, (16, 84))
        plt.ylim(3 * L - 2 * H, 3 * H - 2 * L)
        plt.show()

'''
# test
# y test value vs. SPACECRAFT_CLOCK_START_COUNT
y = metadata[:,80].reshape(5460,1)
plt.plot(time, y, "o", markersize=4)
plt.ylabel('y input test')
plt.xlabel('SPACECRAFT_CLOCK_START_COUNT (units???)')
plt.suptitle("y test vs. SPACECRAFT_CLOCK_START_COUNT")
plt.title('Volume COISS 2052', fontsize=10)
plt.ylim(-100, 100)
plt.show()
'''
# annotate each point with the target name
# for plots where y value is target
# plt.txt items?
# find related metadata


# double check units

# which plots look like smooth functions vs random vs uninteresting?
    # Declination
    # Maximum ring radius? = not much really
    # Minimum ring radius? = not much really
    # Phase angle
    # Pixel scale
    # Planet center? (x and y) = not much really
    # Right ascension
    # all the position and velocity vectors = VERY SMOOTH
    # sub solar latitude (longitude one is weird)
    # sub spacecraft latitude (longitude one is weird)
    # target distance
    # twise angle
    

# most of the longitude and latitude plots are still dotted lines??
# also several of the angles?



# pick images from csv
# look up image in PDS Image Atlas
# browse image
# browse == html
# paste into Ana's code
# copy link of label

# first 5 
# middle 5
# last 5

# check time stamp
# check if images make sense




























