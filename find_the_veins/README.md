# Find the Veins - Image processing

The goal for this section of the hackathon is to attempt to find the "veins" within the acceptable bands provided within the HDR/IMG files.

We will need to represent the different wavelength bands as separate images and attempt through CV to find an acceptable process that can attempt to automate the finding of these "veins".

## Pre-requesite
Install:
- `python` version `>= 2.7.13`
- `python-pip`
- `python-cv`
- `apt-get install ffmpeg`
- `apt-get install zlib1g-dev`
- `apt-get install python-tk`
- `apt-get install libsm6 libxext6`

## Python requirements
- `pip install numpy`
- `pip install spectral`

### displayHDRImage.py

This needs:
```
hdr='<location-to-HDR-file>' \
img='<location-to-IMG-file>' \
outgoing_images_path='<directory-to-save>' \
outgoing_file_name='<name-of-file>'
# optional - if set to True, it will not render the full rows/columns, but a pre-determined cropped version
cropped=True \
python displayHDRImage.py
```

 What this does is it will run through the predefined bands that are free of artifacts, but render all of the rows and columns (lines and samples) as a single image in varying degrees of RGB changes (from [0,0,0] -> [255,255,255]).

The files generated will have appended `_000.jpg` in ascending order until `255`.

The purpose after this is to then be able to run the following:

```
cd <outgoing_images_path> &&
ffmpeg -pattern_type glob \
    -i '*.jpg' \
    -vf fps=60 \
    -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    compiled_HDR_animation.mp4
```

which can piece together all the images and render a final animation as an `.mp4`.

### contourAnalysisFile.py & contourAnalysisMultipleFiles.py

These scripts need similar commands in order to run:

`contourAnalysisFile`
```
incoming_image_path='<location-of-image>' \
outgoing_image_path='<location-of-final-image>' \
outgoing_file_name='<name-of-file>' \
python contourAnalysisFile.py
```

`contourAnalysisMultipleFiles`
```
incoming_images_path='<location-of-image>' \
outgoing_images_path='<location-of-final-image>' \
outgoing_file_name='<name-of-file>' \
python contourAnalysisMultipleFiles.py
```

What both of these scripts do is that it takes the generated images from the `displayHDRImage.py` and does the following to each of them:

- Reads the image
- Converts the image to greyscale
- Blurs the greyscale images using GaussianBlur via some values
- Creates a temporary threshold image based on some threshold values (this needs tweeking)
- Contour values are generated around these threshold perimeters
- Before the final contour drawings are generated, PCA is used: https://docs.opencv.org/3.4.3/d1/dee/tutorial_introduction_to_pca.html to determine if the contour graphs themselves have a "strong" linear dataset
- A new image is produced where the contour drawings _should_ wrap around the veins on each band.

#### Issues
- These contour drawings should most likely be in a different format for what the stakeholder would like, but currently we are generating a simple .jpg for now.
- The contour drawings should be weighed against all the other bands to determine definitively if there is a vein throughout the image file.
