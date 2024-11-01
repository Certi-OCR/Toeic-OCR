import cv2
import numpy as np

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blur, 30, 200)
    return canny

def get_transformed_image(image, points):
    points = points.reshape((4, 2))
    input_points = np.zeros((4, 2), dtype="float32")
    points_sum = points.sum(axis=1)
    input_points[0] = points[np.argmin(points_sum)]
    input_points[3] = points[np.argmax(points_sum)]
    diff = np.diff(points, axis=1)
    input_points[1] = points[np.argmin(diff)]
    input_points[2] = points[np.argmax(diff)]
    
    (topL, topR, bottomL, bottomR) = input_points
    bottom_width = np.sqrt(((bottomR[0] - bottomL[0]) ** 2) + ((bottomR[1] - bottomL[1]) ** 2))
    top_width = np.sqrt(((topR[0] - topL[0]) ** 2) + ((topR[1] - topL[1]) ** 2))
    right_height = np.sqrt(((topR[0] - bottomR[0]) ** 2) + ((topR[1] - bottomR[1]) ** 2))
    left_height = np.sqrt(((topL[0] - bottomL[0]) ** 2) + ((topL[1] - bottomL[1]) ** 2))
    
    max_width = max(int(bottom_width), int(top_width))
    max_height = max(int(right_height), int(left_height))
    
    converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
    matrix = cv2.getPerspectiveTransform(input_points, converted_points)
    img_output = cv2.warpPerspective(image, matrix, (max_width, max_height))
    return img_output

def main():
    img_org = cv2.imread('Original.jpg')
    if img_org is None:
        print("Error: Image not found.")
        return
    
    img_copy = img_org.copy()
    canny = preprocess_image(img_copy)
    
    contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    biggest = biggest_contour(contours)
    
    if biggest.size == 0:
        print("Error: No suitable contour found.")
        return
    
    cv2.drawContours(img_copy, [biggest], -1, (0, 255, 0), 2)
    img_output = get_transformed_image(img_org, biggest)
    
    canny = np.stack((canny,) * 3, axis=-1)
    img_stacked = np.hstack((canny, img_copy))
    
    cv2.imshow('Stacked Images', img_stacked)
    cv2.imshow('Output Image', img_output)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()