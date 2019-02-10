import numpy as np
import cv2 as cv
import os
import glob
from math import atan2, cos, sin, sqrt, pi

INCOMING_IMAGE_PATH = os.environ['incoming_image_path']
OUTGOING_IMAGE_PATH = os.environ['outgoing_image_path']
OUTGOING_FILE_NAME = os.environ['outgoing_file_name']

# hella lifted from: https://docs.opencv.org/3.4.3/d1/dee/tutorial_introduction_to_pca.html
def getOrientation(pts, img):
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i,0] = pts[i,0,0]
        data_pts[i,1] = pts[i,0,1]
    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv.PCACompute2(data_pts, mean)
    # Store the center of the object
    cntr = (int(mean[0,0]), int(mean[0,1]))
    
    # cv.circle(img, cntr, 3, (255, 0, 255), 2)
    p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
    p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
    # drawAxis(img, cntr, p1, (0, 255, 0), 1)
    # drawAxis(img, cntr, p2, (255, 255, 0), 5)
    angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
    
    return angle, (cntr[0] - p1[0], cntr[1] - p1[1]), (cntr[0] - p2[0], cntr[1] - p2[1])

# Contours
img = cv.imread(INCOMING_IMAGE_PATH)
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # convert to gray
img_blurred = cv.GaussianBlur(img_gray, (7, 7), 2)
thresh = cv.threshold(img_blurred, 55, 255, cv.THRESH_BINARY)[1]
contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

filteredContours = []
for cnt in contours:
    area = cv.contourArea(cnt)
    if (area > 90 and area < 4200):
        angle, first_pt, second_pt = getOrientation(cnt, img)

        if (abs(first_pt[0]) > 5): # abstract number, I just picked it randomly
            filteredContours.append(cnt)

img = cv.drawContours(img, filteredContours, -1, (0, 255, 0), 3)
cv.imwrite("{OUTGOING}/{OUTGOING_FILE_NAME}.jpg"
    .format(
        OUTGOING=OUTGOING_IMAGE_PATH, 
        OUTGOING_FILE_NAME=OUTGOING_FILE_NAME
    ), img)
