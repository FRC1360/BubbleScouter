import numpy as np
import cv2 as cv

#By: Ethan Childerhose
#Written July 30th, 2018
#
#TODO create sheet
#TODO add restful upload
#TODO add scanner transfer protocol

#all measurements in pixels

#Circle Filtering Tolerances
minCircle = 30
maxCircle = 50

#minimum distance circles can be to each other
minCircleDis = 80

#row and column grouping tolerances
rowTolerance = 40
colTolerance = 40

#circle radius
radius = 0

#Verifies if a circle is in a given row or column
def isInList(tolerance, list, item):
    for i in list:
        if(abs(int(i) - int(item)) <= tolerance):
            return True

    return False

#Find circles in image
def getCircles(image):
    circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 1, minCircleDis, param1=22, param2=30, minRadius=minCircle, maxRadius=maxCircle)

    circles = np.uint16(np.around(circles))

    return circles

#find rows
def getRowCords(cricles, v):
    row = []

    for circle in circles[0]:
        if(len(row) == 0):
            row.append(circle[1])

        if (not isInList(rowTolerance, row, circle[1])):
            row.append(circle[1])

    row.sort()

    if(v):
        print(row)

    return row

#find columns
def getColCords(circles, v):
    col = []

    for circle in circles[0]:
        if(len(col) == 0):
            col.append(circle[0])

        if(not isInList(colTolerance, col, circle[0])):
            col.append(circle[0])

    col.sort()

    if(v):
        print(col)

    return col

#find avg circle radius
def getRadius(circles, v):
    avg = 0

    for circle in circles[0]:
        avg += circle[2]

    if(v):
        print(avg / len(circles[0]))

    return avg / len(circles[0])

#generate true false list for circles
def generateMasterList(cols, rows, img):

    master = []

    for i in rows:
        tempList = []
        for q in cols:
            height,width = img.shape
            mask = np.zeros((height,width), np.uint8)

            cv.circle(mask, (q, i),radius, 255, 1)
            print("Mask Val = " + str(cv.mean(img, mask)[0]) + ", x = " + str(q) + ", y = " + str(i))
            if(cv.mean(img, mask)[0] < 100):
                print("TRUE FOUND", q, i)
                tempList.append(True)
            else:
                tempList.append(False)

        master.append(tempList)

    return master

#read in the image
img = cv.imread("printedSheet.jpg", 0)

#scale image down
img = cv.resize(img, (0,0), fx=0.25, fy=0.25)

#colour image for output
imgClr = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

#get circles
circles = getCircles(img)

#get rows and columns
cols = getColCords(circles, True)
rows = getRowCords(circles, True)

#get circles radius
radius = getRadius(circles, False)

#generate master
mast = generateMasterList(cols, rows, img)
print(mast)

#overlay master on original image
for x in range(len(mast)):
    for y in range(len(mast[0])):
        if(mast[x][y]):
            cv.circle(imgClr, (cols[y], rows[x]), radius, (0, 255, 0), 2)
        else:
            cv.circle(imgClr, (cols[y], rows[x]), radius, (255, 0, 0), 2)

#show everything
cv.imshow('detected circles', imgClr)
cv.waitKey(0)
cv.destroyAllWindows()