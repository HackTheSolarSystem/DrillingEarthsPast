# Renders all of the specified bands
# and runs through all the RGB values from 0 -> 255

from spectral import *
import spectral.io.envi as envi
import os

HDR_File = os.environ['hdr']
IMG_File = os.environ['img']

img = envi.open(HDR_File, IMG_File)

totalLines = img.shape[0]
totalSamples = img.shape[1]
totalBands = img.shape[2]

bandsToRead = []
for i in range(18, 274):
    bandsToRead.append(i)

subRegion = img.read_subregion(
    (0, totalLines),
    (0, totalSamples),
    bandsToRead
)

for i in range(256): # 255 RGB Value max
    save_rgb('images/rgb/rgb_{num:03d}.jpg'.format(num=i), # Naming convention used for ffmpeg conversion
        subRegion,
        [i, i, i]
    )
