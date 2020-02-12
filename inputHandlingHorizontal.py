import cv2
import numpy as np
import os
# TODO - make it into a function that has an arg = path(str)
# TODO - try to compare to min instead of mean
path = ".\\resources\\img02\\"                                         # image location

images = []                                                            # get all the image names in the directory
for r, d, f in os.walk(path):                                          # r=root, d=directories, f = files
    for file in f:
        if '.jpg' in file:
            if 'el' not in file:
                images.append(file)

elementNumber = 0                                                     # indexing number for extracted elements
for image_name in images:                                             # process every slice
    img = cv2.imread(path + image_name)                               # read the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                      # convert the img to grayscale

    H, W = img.shape[:2]                                              # image dimensions
    imgMean = np.mean(img)                                            # find the mean of the image

    for i in range(len(img[0])):                                      # go horizontally; len(img[0]) = no. of columns
        columnMean = 0                                                # calculate the mean of every column
        for j in range(len(img)):
            columnMean = columnMean + np.mean(img[j][i])              # add the means of all the pixels in a column
        columnMean = columnMean / len(img)                            # divide by the number of elements(rows) in column
        if columnMean > imgMean:                                      # cut away the spaces before score lines
            img = img[0:H, i:len(img[0])]                             # crop the image
            break                                                     # break when done

    for i in range(len(img[0]) - 1, 0, -1):                           # go backwards (end to 0, with step being -1)
        columnMean = 0                                                # calculate the mean of every column
        for j in range(len(img)):
            columnMean = columnMean + np.mean(img[j][i])             # add the means of all the pixels in a column
        columnMean = columnMean / len(img)                           # divide by the number of elements(rows) in column
        if columnMean > imgMean:                                     # cut away the spaces after score lines
            img = img[0:H, 0:i]                                      # crop the image
            break                                                    # break when done

    imgMean = np.mean(img)                                           # find the new mean of the image
    xCutStart = [0]                                                  # coordinates for the left side of the element
    xCutEnd = []                                                     # coordinates for the right side of the element
    stillLess = False                                                # flag = if the vertical line is less than mean

    for i in range(len(img[0])):                                     # go horizontally; len(img[0]) = no. of columns
        columnMean = 0                                               # calculate the mean of every column
        for j in range(len(img)):
            columnMean = columnMean + np.mean(img[j][i])             # add the means of all the pixels in a column
        columnMean = columnMean / len(img)                           # divide by the number of elements(rows) in column

        if columnMean * 1.1 >= imgMean:                              # find the starting coordinate of a cropped picture
            if stillLess is True:
                xCutStart.append(i)
            stillLess = False

        if columnMean * 1.1 < imgMean:                               # find the ending coordinate of a cropped picture
            if stillLess is False:
                xCutEnd.append(i)
            stillLess = True

    xCutEnd.append(len(img[0]) - 1)                                 # the last cutting coordinate is the end of  image

    for i in range(len(xCutStart)):
        element = img[0:H, xCutStart[i]:xCutEnd[i]]         # cut the element from the image
        elementName = "el" + str(elementNumber).zfill(5) + ".jpg"   # generate the element name
        if len(element[0]) > 5:
            try:                                                        # if an element is not null
                cv2.imwrite(path + elementName, element)                # save the elements in the directory
            except:                                                     # else, skip that element
                pass
            elementNumber = elementNumber + 1                           # increase the indexing number

for fileName in os.listdir(path):                                   # delete redundant images from the previous step
    if fileName.startswith("slice"):
        os.remove(os.path.join(path, fileName))
