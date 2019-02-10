# DrillingEarthsPast
Addressing [Drilling Earth's Past Project](https://github.com/amnh/HackTheSolarSystem/wiki/Drilling-Into-Earth's-Past)

## Created by `#notacircle`
* [Sarah Nagy](https://github.com/sarahrn)
* [Camera Ford](https://github.com/CamFord16)
* [Erika Samuels](https://github.com/e-r-i-k-a)
* [Hector Leiva](https://github.com/hectorleiva)

## Solutions

The automatic detection of veins was approached by transforming the cubic `.img` files into a series of JPEG images that would then be analyzed using OpenCV. OpenCV's process was written such that each image was slightly blurred, greyscaled, a filter was added for threshold values where the pixel differences would be more extreme. After this we added a Principal Component Analysis (PCA) stat procedure to identify "semi-linear" "lines" and then drew contours around those.

Classifying the Mineral Spectra was solved by removing the artifacts from the `.img` files (wavelengths less than 1000, more than 2400) and then normalized and data smoothed out. We validated 20 samples taken from the `.img` files with our stakeholder Rebecca to have a clean, labelled data set. With this dataset, a model was built out to then compare against the `.img` wave spectrum files and probability rankings were returned with the highiest confidence in identified minerals at the top.

## Installation Instructions

Install:
- `python` version `>= 2.7.13`
- `apt-get install python-pip`
- `apt-get install python-cv`
- `apt-get install ffmpeg`
- `apt-get install zlib1g-dev`
- `apt-get install python-tk`
- `apt-get install libsm6 libxext6`

## Python requirements
- `pip install numpy`
- `pip install spectral`