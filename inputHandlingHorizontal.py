import cv2
import numpy as np
import os

path = ".\\resources\\img02\\"  # image Name

# get the images
images = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.jpg' in file:
            if 'rotated' not in file:
                images.append(file)
                break #makni ovo kasnije

for image_name in images:
    img = cv2.imread(path + image_name)
    # Convert the img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 30, maxLineGap=250)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 128), 1)

    H, W = img.shape[:2]

    start_point = (0, 0)         #x,y
    end_point = (250, 250)
    color = (0, 255, 0)         # Green color in BGR
    thickness = 9               # Line thickness of 1 px



    imgMean = np.mean(img)
    for i in range(len(img[0])):
        columnMean = 0
        for j in range(len(img)):
            columnMean = columnMean + np.mean(img[j][i])
        columnMean = columnMean / len(img)
        print(columnMean)
        if columnMean < imgMean:
            start_point = (i, 0)
            end_point = (i, H)
            cv2.line(img, start_point, end_point, color, thickness)



    # for lineIndex, hLine in enumerate(img):
    #     for pixelIndex, pixel in enumerate(hLine):
    #         if np.mean(pixel) > imgMean:
    #             print(pixel)
    #             start_point = (pixelIndex - 20, 0)
    #             end_point = (pixelIndex - 20, H)
    #             cv2.line(img, start_point, end_point, color, thickness)
    #             break

    cv2.imshow("linesEdges", edges)
    cv2.imshow("linesDetected", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
