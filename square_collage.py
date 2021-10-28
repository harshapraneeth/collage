import os
import cv2
import numpy as np

# --------- get inputs ---------

print("enter the name of the input image: ", end="")
input_filename = input().strip()

print("enter the folder with the images: ", end="")
inputs_folder = input().strip()

print("save as: ", end="")
output_name = input().strip()

min_output_size = 3600
cell_size = 80
overlay_opacity = 0.25

# --------- load inputs ---------

print("loading inputs...", end=" ")

input_images = [
    cv2.resize(cv2.imread(inputs_folder+"/"+image), (cell_size, cell_size))
    for image in os.listdir(inputs_folder)
]
n_images = len(input_images)

print("done")

# --------- calculating averages ---------

print("calculating input averages...", end=" ")

input_avgs = tuple(
    tuple(map(int, image.mean(axis=(0, 1)))) 
    for image in input_images
)

# --------- resizing the input to target size ---------

input_image = cv2.imread(input_filename, cv2.IMREAD_COLOR)

target_shape = list(input_image.shape)

if(target_shape[0]<min_output_size):
    target_shape[1] = target_shape[1]*round(min_output_size/target_shape[0])
    target_shape[0] = min_output_size

if(target_shape[1]<min_output_size):
    target_shape[0] = target_shape[0]*round(min_output_size/target_shape[1])
    target_shape[1] = min_output_size

target_shape[0] = round(target_shape[0]/cell_size)*cell_size
target_shape[1] = round(target_shape[1]/cell_size)*cell_size


input_image = cv2.resize(input_image, (target_shape[1], target_shape[0]))

print("done")

# --------- some helper functions ---------

distance = lambda a, b : ((a[0]-b[0])**2) + ((a[1]-b[1])**2) + ((a[2]-b[2])**2)

def nearest(x):
    min_i, min_d = 0, distance(x, input_avgs[0])
    for i in range(1, n_images):
        d = distance(x, input_avgs[i])
        if d<min_d: min_i, min_d = i, d
        if min_d==0: break
    return min_i

# --------- creating the collage ---------

print("creating collage...")
print("progress: 0 %", end="\r")

for row in range(0, input_image.shape[0], cell_size):
    for col in range(0, input_image.shape[1], cell_size):
        target_avg = tuple(map(
            int,
            input_image[row:row+cell_size, col:col+cell_size].mean(axis=(0, 1))
        ))
        input_image[row:row+cell_size, col:col+cell_size] = (input_image[row:row+cell_size, col:col+cell_size]*overlay_opacity).astype(np.uint8)
        input_image[row:row+cell_size, col:col+cell_size] += (input_images[nearest(target_avg)]*(1-overlay_opacity)).astype(np.uint8)
    print("progress:",round(row*100/input_image.shape[0], 2),"%     ", end="\r")

print("progress: 100 %     ")

if(cv2.imwrite(output_name, input_image)): print("collage saved")
else: print("failed to save the image")