# Mineral Classifier

The goal for this section of the hackathon is to attempt to find the "veins" within the acceptable bands provided within the HDR/IMG files.

We will need to represent the different wavelength bands as separate images and attempt through CV to find an acceptable process that can attempt to automate the finding of these "veins".

## Pre-requesite
Install:
- `conda create -n drillingearthspast python=3.7`

## Python requirements
- `pip install numpy`
- `pip install spectral`
- `pip install Pillow`

### classify_image.py

This script needs the following directory and image files in ENVI format:

```
Data/
    usgs_min.hdr # Header for pure mineral spectra
    usgs_min.sli # Bands/reflectance for pure mineral spectra
    Ex[image file number].hdr # Header for image spectra
    Ex[image file number].img # Image data for image spectra
```

To run, simply type `python classify_image.py [image file number]`.

This will generate two files:

```
img[image file number]_processed.pickle # Pickle file with smoothed/normalized image spectra
img[image file number]_similarity_scores.pickle # Pickle file with dataframe of mineral similarity scores
```

#### Issues
- Dataframes can get too large to be joined for all ~4000x200 pixels
- Need to speed this up from ~45 minutes per image
