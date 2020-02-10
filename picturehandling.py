import cv2
import numpy as np

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
up_array = np.asarray(upperBound)                                                    # list to array conversion
up = (H - up_array)
low_array = np.asarray(lowerBound)
low = (H - low_array)

slices = []

for i in range(len(up_array)):                                                     # row slicing
    if(low_array[i] + 1) + int(H/350) < H and up_array[i] - int(H / 70) > 0:       # expand the slice vertically
        h_slice = rotated[up_array[i] - int(H / 70):(low_array[i] + 1) + int(H / 350), 0:W]
    else:                                                                          # don't expand on the edges
        h_slice = rotated[up_array[i]:(low_array[i] + 1), 0:W]
    slices.append(h_slice)

# on standard A4 paper(21 cm height), 1 note line is 1 cm -> 1/21 ~= 0.04, so ignore smaller slices
slices[:] = [s for s in slices if not len(s) < 0.04 * H]

valid_slices_pixel_mean = []
for s in slices:
    valid_slices_pixel_mean.append(np.mean(s))

mean = np.mean(valid_slices_pixel_mean)

j = 0
for i in range(len(slices)):                                                        # save the valid slices
    # the slices with notes have approximately the same mean of pixels, ignore the lines that stand out (+- 15% of mean)
    if 1.15 * mean > valid_slices_pixel_mean[i] > 0.85 * mean:
        sliceName = "slice" + str(j) + ".jpg"                                       # slice naming
        cv2.imwrite('resources/' + sliceName, slices[i])
        j = j + 1


