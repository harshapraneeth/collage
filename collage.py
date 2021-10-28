import os
import cv2
import math
import numpy as np

# --------- get inputs ---------

print("enter the name of the input image: ", end="")
input_filename = input().strip()

print("enter the folder with the images: ", end="")
inputs_folder = input().strip()

print("save as: ", end="")
output_name = input().strip()

min_output_size = 3600
cell_size = 40
max_cell_size = cell_size*3
overlay_opacity = 0.25

# --------- load inputs ---------

print("loading inputs...", end=" ")

input_images, input_sizes = [], []
for file in os.listdir(inputs_folder):
    image = cv2.imread(inputs_folder+"/"+file)
    
    size = list(image.shape)

    if size[0]>max_cell_size:
        size[1] = size[1]*(max_cell_size/size[0])
        size[0] = max_cell_size
    
    if size[1]>max_cell_size:
        size[0] = size[0]*(max_cell_size/size[1])
        size[1] = max_cell_size

    size[0] = round(size[0]/cell_size)
    size[1] = round(size[1]/cell_size)

    if size[0]==0 or size[1]==0: size = [1, 1]

    image = cv2.resize(
        image,
        (
            size[1]*cell_size,
            size[0]*cell_size
        )
    )
    input_images.append(image)
    input_sizes.append(size)

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

n_cells = round(target_shape[0]/cell_size), round(target_shape[1]/cell_size)
occupied = [[0 for _ in range(n_cells[1])] for _ in range(n_cells[0])]

print("done")

# --------- some helper functions ---------

distance = lambda a, b : ((a[0]-b[0])**2) + ((a[1]-b[1])**2) + ((a[2]-b[2])**2)

def available(row, col, size):
    for x in range(row, row+size[0]):
        for y in range(col, col+size[1]):
            try:
                if occupied[x][y]: return False
            except: return False
    return True

def nearest(row, col):
    min_d, min_i = math.inf, -1
    
    for i in range(n_images):
        size = input_sizes[i]
        if not available(row, col, size): continue
        d = distance(
            input_image[
                row*cell_size:(row+size[0])*cell_size, 
                col*cell_size:(col+size[1])*cell_size
            ].mean(axis=(0,1)),
            input_images[i].mean(axis=(0, 1))
        )
        if d<min_d: min_d, min_i = d, i

    if min_i>-1: return input_images[min_i], input_sizes[min_i]
    return None, None


# --------- creating the collage ---------

print("creating collage...")
print("progress: 0 %", end="\r")

for row in range(n_cells[0]):
    for col in range(n_cells[1]):
        if occupied[row][col]: continue
        image, size = nearest(row, col)
        if size==None: continue
        input_image[
            row*cell_size:(row+size[0])*cell_size, 
            col*cell_size:(col+size[1])*cell_size
        ] = (input_image[
                row*cell_size:(row+size[0])*cell_size, 
                col*cell_size:(col+size[1])*cell_size
            ]*overlay_opacity).astype(np.uint8)
        input_image[
            row*cell_size:(row+size[0])*cell_size, 
            col*cell_size:(col+size[1])*cell_size
        ] += (image*(1-overlay_opacity)).astype(np.uint8)
        for x in range(row, row+size[0]):
            for y in range(col, col+size[1]): occupied[x][y] = 1
    print("progress:",round(row*100/n_cells[0], 2),"%     ", end="\r")

print("progress: 100 %     ")

if(cv2.imwrite(output_name, input_image)): print("collage saved")
else: print("failed to save the image")