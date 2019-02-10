import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import IPython.display 
from PIL import Image

from scipy.stats import pearsonr
import scipy.signal

import spectral.io.envi as envi

from tqdm import tqdm

import pickle

import sys

def normalize(series):
    return (series - series.min())/(series.max() - series.min())

def derivitize(series):
    return series.pct_change()

def savgol(series):
    return scipy.signal.savgol_filter(series.values,25,4)

def process(series):
    return series.apply(normalize).apply(savgol).values

def get_pure_spectra_library():
    img = envi.open('Data/usgs_min.hdr', 'Data/usgs_min.sli')
    spectra = pd.DataFrame(img.spectra, index=img.names, columns=[x*1000 for x in img.bands.centers]).T
    spectra = spectra[(spectra.index > 1000) & (spectra.index < 2540)]
    for column in spectra.columns:
        spectra[column] = spectra[[column]].apply(normalize).apply(savgol).values
    return spectra

def run(img_number):
    ##########################
    # Get pure mineral spectra
    ##########################
    spectra = get_pure_spectra_library()

    ##################
    # Clean image data
    ##################
    hdr = 'Data/Ex' + str(img_number) + '.hdr'
    img = 'Data/Ex' + str(img_number) + '.img'

    img = envi.open(hdr, img)

    x_pixel_range = range(0,img.shape[0])
    y_pixel_range = range(0,img.shape[1])

    pixel_classification_dict = {}

    wavelength = img.bands.centers
    good_wavelengths_mask = [x for x in range(0,len(wavelength)) if wavelength[x] > 1000 and wavelength[x] < 2400]
    wavelength = [wavelength[x] for x in good_wavelengths_mask]

    processed_data = {}

    for x in tqdm(x_pixel_range):
        for y in y_pixel_range:
        
            reflectance = img.read_pixel(x, y)

            reflectance = reflectance[good_wavelengths_mask[0]:(good_wavelengths_mask[-1]+1)]
            reflectance = normalize(reflectance)
            reflectance = scipy.signal.savgol_filter(reflectance,25,4)
        
            processed_data[x,y] = reflectance

    spectrum = pd.DataFrame(processed_data)
    spectrum.index = wavelength

    # Pickle image 
    pickle.dump(spectrum, open("img" + str(img_number) + "_procssed.pickle", "wb"))

    #############################################
    # Join pure mineral spectra and image spectra
    #############################################
    basic_index = pd.DataFrame(index=range(1000,2540))
    spectrum.index = [round(x) for x in spectrum.index]
    spectra.index = [round(x) for x in spectra.index]
    joined_spectra = pd.concat([basic_index,spectrum,spectra],axis=1).interpolate().bfill()

    spectra_cleaned = joined_spectra.iloc[:,:spectrum.shape[1]]
    spectrum_cleaned = joined_spectra.iloc[:,spectrum.shape[1]:]

    ####################################################
    # Calculate mineral similarity scores for each pixel
    ####################################################
    results_dict = {}

    for i in tqdm(range(0,spectra_cleaned.shape[1])):
        spectra_slice = joined_spectra.iloc[:,[i] + list(range(spectra_cleaned.shape[1],joined_spectra.shape[1]))]
        results_dict[i] = np.corrcoef(spectra_slice.T.values)[0][1:]

    pickle.dump(results_dict, open("img" + str(img_number) + "_similarity_scores.pickle", "wb"))

if __name__ == "__main__":
    run(sys.argv[0])