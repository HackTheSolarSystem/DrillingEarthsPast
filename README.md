# DrillingEarthsPast
Addressing [Drilling Earth's Past Project](https://github.com/amnh/HackTheSolarSystem/wiki/Drilling-Into-Earth's-Past)

## Created by `#notacircle`
* [Sarah Nagy](https://github.com/sarahrn)
* [Camera Ford](https://github.com/CamFord16)
* [Erika Samuels](https://github.com/e-r-i-k-a)
* [Hector Leiva](https://github.com/hectorleiva)

## Solutions

The automatic detection of veins was approached by transforming the cubic `.img` files into a series of JPEG images that would then be analyzed using OpenCV. OpenCV's process was written such that each image was slightly blurred, greyscaled, a filter was added for threshold values where the pixel differences would be more extreme. After this we added a Principal Component Analysis (PCA) stat procedure to identify "semi-linear" "lines" and then drew contours around those.

Classifying the Mineral Spectra was solved by removing wavelengths prone to distortion from artifacts from the `.img` files (wavelengths less than 1000, more than 2400) and then normalizing and smoothing the specrtum data. We collected 20 random samples from the `.img` files by asking our stakeholder Rebecca to label them, which gave us a clean, labelled data set we could use to validate our unsupervised model. With this dataset, a model was built out to then compare against the `.img` wave spectrum files and similarity score rankings were returned for each mineral in our mineral spectrum dataset.

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