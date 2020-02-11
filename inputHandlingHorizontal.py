import cv2
import numpy as np
import os
from scipy import ndimage

path = ".\\resources\\img01\\"                                                             # image Name

images = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.jpg' in file:
            if 'rotated' not in file:
                images.append(file)

for image in images:
    img = cv2.imread(path + image)
    # rotation angle in degree
    rotated = ndimage.rotate(img, -90)
    imgName = path + "rotated" + image
    cv2.imwrite(imgName, rotated)

for image in images:
    img = cv2.imread(path + image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # transform into gray img

    th, thr = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # pixels have 1 of 2 values
    nonZeroElements = cv2.findNonZero(thr)  # find the non zero pixels
    nonZeroMinArea = cv2.minAreaRect(nonZeroElements)  # mark the area

    (cx, cy), (w, h), ang = nonZeroMinArea  # find rotated matrix
    if w > h:
        w, h = h, w
        ang += 90

    M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)  # do the rotation
    rotated = cv2.warpAffine(thr, M, (img.shape[0], img.shape[0]))

    hist = cv2.reduce(rotated, 1, cv2.REDUCE_AVG).reshape(-1)  # reduce matrix to a vector

    th = 1  # change the threshold (empirical)
    H, W = img.shape[:2]  # picture dimensions

    upperBound = [y for y in range(H - 1) if hist[y] <= th < hist[y + 1]]  # upper bounds
    lowerBound = [y for y in range(H - 1) if hist[y] > th >= hist[y + 1]]  # lower bounds

    for y in upperBound:
        cv2.line(rotated, (0, y), (W, y), (255, 0, 100), 1)  # (slika, 1.tocka, 2.tocka, boja, debljina)

    for y in lowerBound:
        cv2.line(rotated, (0, y), (W, y), (80, 30, 255), 1)

    cv2.imwrite(image+"RESULT.png", rotated)

    # rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)  # rotated img color conversion
    # up_array = np.asarray(upperBound)  # list to array conversion
    # up = (H - up_array)
    # low_array = np.asarray(lowerBound)
    # low = (H - low_array)
    #
    # slices = []
    # for i in range(len(up_array)):  # row slicing
    #     h_slice = rotated[up_array[i]:(low_array[i] + 1), 0:W]
    #     slices.append(h_slice)  # save all the slices in a list
    #
    # j = 0
    # for i in range(len(slices)):  # save the valid slices
    #     # wanted slices have approximately the same mean of pixels, ignore the unwanted lines(+- 15% of mean)
    #     sliceName = "element" + str(j) + ".jpg"  # slice naming
    #     cv2.imwrite(path + sliceName, slices[i])  # save the slices in that directory
    #     j = j + 1  # name slices iteratively
    #
    #
