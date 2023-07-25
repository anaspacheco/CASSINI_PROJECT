# Cassini Tools - Image and Metadata Processing

This repository contains the following files:

## image_model.py

**Description**: 
The `image_model.py` file downloads a simulation of the given image from http://space.jpl.nasa.gov/. Please edit the file with the HTML of your desired image. 

Much of the code was given by https://github.com/kmgill/cassini_processing, but changes were made to avoid the use of the ISIS3 software and to simplify the process.

### Usage: getmodel.py [-h] -d DATA [-f FOV] [-p PCT]

```python 
optional arguments:
  -h, --help            show this help message and exit
  -f FOV, --fov FOV     Field of view (angle)
  -p PCT, --pct PCT     Body width as percentage of image
