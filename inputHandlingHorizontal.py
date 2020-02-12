import cv2
import numpy as np
import os

path = ".\\resources\\img02\\"                                         # image location

images = []                                                            # get all the images in the directory
for r, d, f in os.walk(path):                                          # r=root, d=directories, f = files
    for file in f:
        if '.jpg' in file:
            images.append(file)
            break #makni ovo kasnije

for image_name in images:                                             # process every slice
    img = cv2.imread(path + image_name)                               # read the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                      # convert the img to grayscale

    H, W = img.shape[:2]                                              # image dimensions

    start_point = (0, 0)                                              # start and end point of a line
    end_point = (0, 0)                                                # format is (x, y) = (0, 0) (for example)
    color = (0, 255, 0)                                               # Green color in BGR
    thickness = 3                                                     # Line thickness of 1 px

    imgMean = np.mean(img)                                            # find the mean of the image

    for i in range(len(img[0])):                                      # go horizontally; len(img[0]) = no. of columns
        columnMean = 0                                                # calculate the mean of every column
        for j in range(len(img)):
            columnMean = columnMean + np.mean(img[j][i])              # add the means of all the pixels in a column
        columnMean = columnMean / len(img)                            # divide by the number of elements(rows) in column
        if columnMean > imgMean:                                      # cut away the spaces before score lines
            # start_point = (i, 0)
            # end_point = (i, H)
            # cv2.line(img, start_point, end_point, color, thickness)
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
    xCutCoordinates = [0]
    stillLess = False
    for i in range(len(img[0])):  # go horizontally; len(img[0]) = no. of columns
        columnMean = 0  # calculate the mean of every column
        for j in range(len(img)):
            columnMean = columnMean + np.mean(img[j][i])  # add the means of all the pixels in a column
        columnMean = columnMean / len(img)  # divide by the number of elements(rows) in column

        if columnMean < imgMean and stillLess is False:  # cut away the spaces before score lines
            # start_point = (i, 0)
            # end_point = (i, H)
            # cv2.line(img, start_point, end_point, color, thickness)
            xCutCoordinates.append(i)
            stillLess = True
        if columnMean >= imgMean and stillLess is True :
            stillLess = False

    sheetElements = []
    for i in range(len(xCutCoordinates) - 1):
        element = img[0:H, xCutCoordinates[i]:xCutCoordinates[i+1]] # crop the image
        sheetElements.append(element)

    for element in sheetElements:
        cv2.imshow("linesDetected", element)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # cv2.imshow("linesDetected", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


