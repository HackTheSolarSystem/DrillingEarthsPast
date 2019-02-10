# Find the Veins - Image processing

The goal for this section of the hackathon is to attempt to find the "veins" within the acceptable bands provided within the HDR/IMG files.

We will need to represent the different wavelength bands as separate images and attempt through CV to find an acceptable process that can attempt to automate the finding of these "veins".

## displayHDRImage.py

This needs:
```
hdr='<location-to-HDR-file>' img='<location-to-IMG-file>'
```

to be defined before running `python displayHDRImage.py`. What this does is it will run through the predefined bands that are free of artifacts, but renders all of the rows and columns (lines and samples) as a single image in varying degrees of RGB changes (from [0,0,0] -> [255,255,255]).

The files generated will be labeled as `rgb_000.jpg` in ascending order until `255`.

The purpose after this is to then be able to run the following:

```
ffmpeg -pattern_type glob -i 'rgb_*.jpg' -vf fps=60 \
-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4
```

which can piece together all the images and render a final animation as an `.mp4`.
