import cv2
import numpy as np
from skimage import io
import sys
from PIL import Image
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

image_filename = "img01.jpg"                                                         # image Name
SongImageOriginal = cv2.imread(image_filename)                                       # read

gray = cv2.cvtColor(SongImageOriginal, cv2.COLOR_BGR2GRAY)                           # transform into gray img
th, thr = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)     # pixels have 1 of 2 values
nonZeroElements = cv2.findNonZero(thr)                                               # find the non zero pixels
nonZeroMinArea = cv2.minAreaRect(nonZeroElements)                                    # mark the area

(cx, cy), (w, h), ang = nonZeroMinArea                                               # find rotated matrix
if w > h:
    w, h = h, w
    ang += 90
M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)                                      # do the rotation
rotated = cv2.warpAffine(thr, M, (SongImageOriginal.shape[1], SongImageOriginal.shape[0]))


hist = cv2.reduce(rotated, 1, cv2.REDUCE_AVG).reshape(-1)                            # reduce matrix to a vector

th = 2
H, W = SongImageOriginal.shape[:2]                                                   # picture dimensions

upperBound = [y for y in range(H - 1) if hist[y] <= th and hist[y + 1] > th]         # upper bounds
lowerBound = [y for y in range(H - 1) if hist[y] > th and hist[y + 1] <= th]         # lower bounds

rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)                                  # rotated img color conversion
# for y in upperBound:
#     cv2.line(rotated, (0, y), (W, y), (255, 0, 100), 1)                            # draw the upper line
# for y in lowerBound:
#     cv2.line(rotated, (0, y), (W, y), (80, 30, 255), 1)                            # draw the lower line

# resultImageName = image_filename + 'RESULT' + '.png';
# cv2.imwrite(resultImageName, rotated)                                                # save the resulting image

up_array = np.asarray(upperBound)                                                    # list to array conversion
up = (H - up_array)
low_array = np.asarray(lowerBound)
low = (H - low_array)

#im = cv2.imread(resultImageName)
im = rotated
for i in range(len(up_array)):                                                     # row slicing
    if(low_array[i] + 1) + int(H/350) < H and up_array[i] - int(H / 70) > 0:
        h_slice = im[up_array[i] - int(H / 70):(low_array[i] + 1) + int(H / 350), 0:W]
    else:
        h_slice = im[up_array[i]:(low_array[i] + 1), 0:W]
    bound = len(up_array)
    name = "slice"                                                                  # slice naming
    name_str = name + str(i)
    cv2.imwrite('resources/'+name_str + ".jpg", h_slice)
    imageIO = io.imread('resources/'+name_str + ".jpg")
    print(np.mean(imageIO))


# im = rotated
# slices = []
# for i in range(len(up_array)):  # row slicing
#     if (low_array[i] + 1) + int(H / 350) < H and up_array[i] - int(H / 70) > 0:
#         slices.append(im[up_array[i] - int(H / 70):(low_array[i] + 1) + int(H / 350), 0:W])
#     else:
#         slices.append(im[up_array[i]:(low_array[i] + 1), 0:W])
#
# # for s in slices:
#
# print(len(slices))
# print(len(slices[0]))
#
# print(len(slices[0][0]))  # = W
# print(len(slices[0][0][0]))
#
# for s in slices:                                                                # iterate over slices
#     pixelSum = 0
#     for i in range(0, len(s)):                                                  # go through all the rows
#         for j in range(0, W):                                                   # go through all the columns
#             if any(s[i][j]) > 0:
#                 pixelSum += sum(s[i][j])/len(s[i][j])                            # add all non zero pixels
#     sliceAvg = pixelSum / (len(s) * W)
#     print(sliceAvg)
#


# broj slice-a, red, stupac


# img=mpimg.imread(hist)
# # imgplot = plt.imshow(img)
# # plt.show()
