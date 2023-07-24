import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime
import rasterio
import imageio
import sys
import pvl

image_id = "N1610585886_1"

#https://planetarydata.jpl.nasa.gov/img/data/cassini/cassini_orbiter/coiss_2050/data/1607482567_1607567228/N1607484037_1.IMG

# Now opening the PDS format (.IMG and .LBL )
with rasterio.open('/Users/anasofiapacheco/Desktop/'+image_id+'.IMG', 'r') as src:
    image_data = src.read(1)


# Plot the image using matplotlib
plt.figure(figsize=(8, 8))
plt.imshow(image_data, cmap='gray')
plt.title(image_id)
plt.xlabel('Pixel Column')
plt.ylabel('Pixel Row')
plt.show()

#Add contour
'''
contour_levels = np.linspace(image_data.min(), image_data.max(), 10) 
plt.contour(image_data, levels=contour_levels, colors='red')
plt.show()
'''

label_file_path ='/Users/anasofiapacheco/Desktop/'+image_id+'.LBL'

# Loading the label file using pvl
with open(label_file_path, 'r') as f:
    label_data = pvl.load(f)

#Next steps: would need to search for this image_id in the large database of all label files (for all volumes -- maybe using MySQL) to find the actual
#metadata that we actually care about 

# Printing the label information
print("Label Information:")
print("===================")
for key, value in label_data.items():
    print(f"{key}: {value}")

#Need to automate this later on
#Note: can find 16-bit greyscale TIFF files at 1024x1024 here: coiss_20XX/extras/tiff/XXXXXXXX_XXXXXXXXX/

'''
image_path = '/Users/anasofiapacheco/Desktop/N1604811666_1.IMG.tiff'

with rasterio.open(image_path) as image:
   image_array = image.read(1)  

# Display the image
plt.imshow(image_array, cmap='gray')  # 'cmap' since image is grayscale
plt.show()
'''

