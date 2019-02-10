# Renders all of the specified bands
# and runs through all the RGB values from 0 -> 255
from spectral import *
import spectral.io.envi as envi
import os

HDR_File_Loc = os.environ['hdr_loc']
IMG_File_Loc = os.environ['img_loc']
OUTGOING_IMAGE_PATH = os.environ['outgoing_images_path']
OUTGOING_FILE_NAME = os.environ['outgoing_file_name']

CROPPED = False

# If 'cropped' is passed, then we'll just take a sub region of the lines/samples
if "cropped" in os.environ:
    CROPPED = os.environ['cropped']

img = envi.open(HDR_File_Loc, IMG_File_Loc)

totalLines = img.shape[0]
totalSamples = img.shape[1]
totalBands = img.shape[2]

bandsToRead = []
for i in range(18, 274): # focus on these bands since the rest produce artifacts
    bandsToRead.append(i)

lines = (20, (totalLines / 2)) if CROPPED else (0, totalLines)
samples = (20, (totalSamples)) if CROPPED else (0, totalSamples)

subRegion = img.read_subregion(
    lines,
    samples,
    bandsToRead
)

for i in range(256): # 255 RGB Value max
    save_rgb(
        '{outgoing_image_path}/{outgoing_file_name}_{num:03d}.jpg'.format(
            outgoing_image_path=OUTGOING_IMAGE_PATH,
            outgoing_file_name=OUTGOING_FILE_NAME,
            num=i
        ), # Naming convention used for ffmpeg conversion
        subRegion,
        [i, i, i]
    )