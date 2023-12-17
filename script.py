import cv2
import matplotlib.pyplot as plt
import csv
import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_file_path.set(file_path)

def read_graph():
    x_range = x_range_entry.get()
    y_range = y_range_entry.get()
    file_path = selected_file_path.get()

    root.destroy()

    image = cv2.imread(file_path, 1)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresholded = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    data_points = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        data_points.append((x, y, w, h))

    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    
    sorted_data_points = sorted(data_points, key=lambda x: x[0])
    x_range = x_range.split('-')
    x_range = [int(value) for value in x_range]

    def divide_interval(start, end, parts):
        interval_size = (end - start + 1) / parts # Calculate the size of each interval
        intervals = [start + interval_size * i for i in range(parts)]  # Create intervals
        return intervals

    intervals = divide_interval(x_range[0], x_range[1], len(data_points))

    y_range = y_range.split('-')
    y_range = [int(value) for value in y_range]

    img_height = image.shape[0]
    with open('output.csv','w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['x-axis','y-axis'])
        for _ in range(len(sorted_data_points)):
            height = sorted_data_points[_][3]/img_height*(y_range[1]-y_range[0])
            y_coor = height+y_range[0]
            csvwriter.writerow([int(intervals[_]),y_coor])


root = tk.Tk()
root.title("Graph Reader")
root.geometry('300x300')

selected_file_path = tk.StringVar()

label = tk.Label(root, text="Select an image:")
label.pack()

button_select = tk.Button(root, text="Open Image", command=open_file_dialog)
button_select.pack()

file_path_label = tk.Label(root, textvariable=selected_file_path)
file_path_label.pack()

x_range_label = tk.Label(root, text="X-axis Range:")
x_range_label.pack()

x_range_entry = tk.Entry(root)
x_range_entry.pack()

y_range_label = tk.Label(root, text="Y-axis Range:")
y_range_label.pack()

y_range_entry = tk.Entry(root)
y_range_entry.pack()

button_read = tk.Button(root, text="Read Graph", command=read_graph)
button_read.pack(pady=10)

root.mainloop()
