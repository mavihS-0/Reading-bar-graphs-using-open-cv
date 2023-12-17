import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv


image = cv2.imread('bar2.png', 1)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresholded = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
print(contours)
data_points = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    data_points.append((x, y, w, h))

cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
plt.imshow(image)
plt.show()
sorted_data_points = sorted(data_points, key=lambda x: x[0])
x_range = input('x-axis range: ').split('-')
x_range = [int(value) for value in x_range]

def divide_interval(start, end, parts):
    interval_size = (end - start + 1) / parts # Calculate the size of each interval
    intervals = [start + interval_size * i for i in range(parts)]  # Create intervals
    return intervals

intervals = divide_interval(x_range[0], x_range[1], len(data_points))

y_range = input('y-axis range: ').split('-')
y_range = [int(value) for value in y_range]

img_height = image.shape[0]
with open('output.csv','w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['x-axis','y-axis'])
    for _ in range(len(sorted_data_points)):
        height = sorted_data_points[_][3]/img_height*(y_range[1]-y_range[0])
        y_coor = height+y_range[0]
        csvwriter.writerow([int(intervals[_]),y_coor])


