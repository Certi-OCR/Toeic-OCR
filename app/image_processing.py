import cv2
import numpy as np

def biggestContour(contours, image):
    biggest = np.array([])
    maxArea = 0
    ExpectedAspectRatio = 2
    imgWidth, imgHeight = image.shape[:2]
    
    for i in contours:
        area = cv2.contourArea(i)
        if area < 1000:
            continue
        perimeter = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
        
        if area > maxArea and len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if w < 0.1 * imgWidth or h < 0.1 * imgHeight:
                continue
            aspectRatio = w / float(h)
            if 0.9 * ExpectedAspectRatio < aspectRatio < 1.1 * ExpectedAspectRatio:
                biggest = approx
                maxArea = area
    return biggest

def preprocessImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    canny = cv2.Canny(thresh, 30, 200)
    return canny

def getTransformedImage(image, points):
    points = points.reshape((4, 2))
    inputPoints = np.zeros((4, 2), dtype="float32")
    pointsSum = points.sum(axis=1)
    inputPoints[0] = points[np.argmin(pointsSum)]
    inputPoints[3] = points[np.argmax(pointsSum)]
    diff = np.diff(points, axis=1)
    inputPoints[1] = points[np.argmin(diff)]
    inputPoints[2] = points[np.argmax(diff)]
    
    (topLeft, topRight, bottomLeft, bottomRight) = inputPoints
    bottomWidth = np.sqrt(((bottomRight[0] - bottomLeft[0]) ** 2) + ((bottomRight[1] - bottomLeft[1]) ** 2))
    topWidth = np.sqrt(((topRight[0] - topLeft[0]) ** 2) + ((topRight[1] - topLeft[1]) ** 2))
    rightHeight = np.sqrt(((topRight[0] - bottomRight[0]) ** 2) + ((topRight[1] - bottomRight[1]) ** 2))
    leftHeight = np.sqrt(((topLeft[0] - bottomLeft[0]) ** 2) + ((topLeft[1] - bottomLeft[1]) ** 2))
    
    maxWidth = max(int(bottomWidth), int(topWidth))
    maxHeight = max(int(rightHeight), int(leftHeight))
    
    convertedPoints = np.float32([[0, 0], [maxWidth, 0], [0, maxHeight], [maxWidth, maxHeight]])
    matrix = cv2.getPerspectiveTransform(inputPoints, convertedPoints)
    imgOutput = cv2.warpPerspective(image, matrix, (maxWidth, maxHeight))
    return imgOutput

def processImage(image):
    imgOrg = np.array(image)
    
    canny = preprocessImage(imgOrg.copy())
    
    contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    biggest = biggestContour(contours, imgOrg)
    
    if biggest.size == 0:
        return imgOrg
        
    imgOutput = getTransformedImage(imgOrg, biggest)
    return imgOutput