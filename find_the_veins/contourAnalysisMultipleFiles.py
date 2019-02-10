# Horrible code and comments left for posterity

import numpy as np
import cv2 as cv
import os
import glob
from math import atan2, cos, sin, sqrt, pi

INCOMING_IMAGES_PATH = os.environ['incoming_images_path']
OUTGOING_IMAGES_PATH = os.environ['outgoing_images_path']
OUTGOING_FILE_NAME = os.environ['outgoing_file_name']

image_files = glob.glob(os.path.join(INCOMING_IMAGES_PATH, "*.jpg"))

# Depreciated, not needed
# def drawAxis(img, p_, q_, colour, scale):
#     p = list(p_)
#     q = list(q_)
    
#     angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
#     hypotenuse = sqrt((p[2] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
#     # Here we lengthen the arrow by a factor of scale
#     q[0] = p[0] - scale * hypotenuse * cos(angle)
#     q[1] = p[1] - scale * hypotenuse * sin(angle)
#     cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)
#     # create the arrow hooks
#     p[0] = q[0] + 9 * cos(angle + pi / 4)
#     p[1] = q[1] + 9 * sin(angle + pi / 4)
#     cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)
#     p[0] = q[0] + 9 * cos(angle - pi / 4)
#     p[1] = q[1] + 9 * sin(angle - pi / 4)
#     cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)

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

# ret,thresh1 = cv.threshold(im,127,255,cv.THRESH_BINARY)
# ret,thresh2 = cv.threshold(im,127,255,cv.THRESH_BINARY_INV)
# ret,thresh3 = cv.threshold(im,127,255,cv.THRESH_TRUNC)
# ret,thresh4 = cv.threshold(im,127,255,cv.THRESH_TOZERO)
# ret,thresh5 = cv.threshold(im,127,255,cv.THRESH_TOZERO_INV)

# images = [thresh1, thresh2, thresh3, thresh4, thresh5]

# for i in xrange(5):
#     cv.imwrite('testimages/test-thresh-{num}.jpg'.format(num=i), images[i])

# img_blur = cv.medianBlur(im, 5)
# ret,th1 = cv.threshold(img_blur,127,255,cv.THRESH_BINARY)
# th2 = cv.adaptiveThreshold(img_blur,255,cv.ADAPTIVE_THRESH_MEAN_C,\
#             cv.THRESH_BINARY,11,2)
# th3 = cv.adaptiveThreshold(img_blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv.THRESH_BINARY,11,2)

# more_images = [th1, th2, th3]
# for i in xrange(3):
#     cv.imwrite('testimages/test-thresh-more-{num}.jpg'.format(num=i), more_images[i])

# Canny Edges - does not seem to work
# for i in range(100):
#     edges = cv.Canny(im, i, 100)
#     cv.imwrite('testimages/test-{num}.jpg'.format(num=i), edges)

# Watershed - I don't even know where to start
# gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
# ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
# cv.imwrite('testimages/test-watershed.jpg', thresh)

# Image Gradients - better, but still not good
# sobelx = cv.Sobel(im, cv.CV_64F, 1, 0, ksize=5)
# img_grey = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
# sobely = cv.Sobel(img_grey, cv.CV_64F, 0, 1, ksize=3)
# laplacian = cv.Laplacian(im,cv.CV_64F, ksize=1)

# sobelx64f = cv.Sobel(im,cv.CV_64F,1,0,ksize=5)
# abs_sobel64f = np.absolute(sobelx64f)
# sobel_8u = np.uint8(abs_sobel64f)

# cv.imwrite('testimages/test-sobelx.jpg', sobelx)
# cv.imwrite('testimages/test-sobely.jpg', sobely)
# cv.imwrite('testimages/test-sobelabs.jpg', sobel_8u)
# cv.imwrite('testimages/testlaplacian.jpg', laplacian)



for i, image_file_loc in enumerate(image_files):
    # image_file = 'images/EX1_Full_Spectrum_Images/rgb_100.jpg'

    # Contours
    img = cv.imread(image_file_loc)
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

    # finalContours = []
    # for i in filteredContours:
    #     angle, first_pt, second_pt = getOrientation(i, img_100)
    #     if (abs(first_pt[0]) > 5): # abstract number, I just picked it randomly
    #         finalContours.append(i)
    img = cv.drawContours(img, filteredContours, -1, (0, 255, 0), 3)
    cv.imwrite("{OUTGOING}/{OUTGOING_FILE_NAME}-{NUM:03d}.jpg"
        .format(
            OUTGOING=OUTGOING_IMAGES_PATH, 
            OUTGOING_FILE_NAME=OUTGOING_FILE_NAME,
            NUM=i
        ), img)
    # cv.imwrite('testimages/test-contour.jpg', img)
