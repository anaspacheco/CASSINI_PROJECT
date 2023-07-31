import csv
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show
import datetime
import rasterio
import imageio
import sys
import pvl
import requests

# URL of the image
image_url = "https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/coiss_2050/data/1607482567_1607567228/N1607484037_1.IMG"

#ImageID (will automate this later on)
image_id = "N1607484037_1"

with rasterio.open(image_url) as dataset:
    image_data = dataset.read(1)  # Single-band image

# Plot the image using matplotlib
#plt.imshow(image_data, cmap='gray', interpolation='nearest')
# Define a threshold for higher brilliance (adjust this value as needed)
threshold = 200

# Find the indices of pixels with brilliance above the threshold
higher_brilliance_indices = np.argwhere(image_data > threshold)

# Calculate the bounding box coordinates (xmin, xmax, ymin, ymax)
xmin, ymin = higher_brilliance_indices.min(axis=0)
xmax, ymax = higher_brilliance_indices.max(axis=0)

# Crop the image to the higher brilliance region
cropped_image_data = image_data[ymin:ymax, xmin:xmax]



#plt.title(image_id)
#plt.xlabel('Pixel Column')
#plt.ylabel('Pixel Row')
plt.imshow(cropped_image_data, cmap='gray', interpolation='nearest')
#plt.show()

#Possibility: add contour
'''
contour_levels = np.linspace(image_data.min(), image_data.max(), 10) 
plt.contour(image_data, levels=contour_levels, colors='red')
plt.show()
'''

#Label of image, to be outputed to a file

label_url = "https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/coiss_2050/data/1607482567_1607567228/N1607484037_1.LBL"

label_response = requests.get(label_url)
label_response.raise_for_status()  # Check if the request was successful
label = label_response.text

# Output the parsed PVL content to a new file
output_file_path = image_id +"_metadata" + ".txt"  # Replace with the desired output file path
with open(output_file_path, "w") as output_file:
    output_file.write(label)

#Next steps: would need to search for this image_id in the large database of all label files (for all volumes -- maybe using MySQL) to find the actual
#metadata that we actually care about 

#Another possibility: can find 16-bit greyscale TIFF files at 1024x1024 here: coiss_20XX/extras/tiff/XXXXXXXX_XXXXXXXXX/

'''
image_path = '/Users/anasofiapacheco/Desktop/N1604811666_1.IMG.tiff'

with rasterio.open(image_path) as image:
   image_array = image.read(1)  

# Display the image
plt.imshow(image_array, cmap='gray')  # 'cmap' since image is grayscale
plt.show()
'''

