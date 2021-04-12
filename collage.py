# To use this program you need atleast 100 input images named 'input (0).jpg', 'input (1).jpg', and so on in a folder names input_images. 
# Or you can name the folder whatever you want and change the variable 'inputs_name' accordingly.
# You can rename all images in this pattern using "select all" and "rename". Select all images in the folder and rename them as "input".
# They will all be renamed as in the above pattern. Make sure they all are in the same format like jpeg, jpg or png. Also enter the correct format in the "inputs_name".

# The inputs folder should be in the same directory as the program itself or you can provide the full path of the input folder in the variable inputs_name.
# The target_name is the name of the image you want to produce from the smaller images and it should be in the same directory as the program. 
# Once you have all the images double click the 'run.bat' file. Or you can run the program from the terminal.


# ---------- importing necessary libraires ---------- 
import cv2
import math
import numpy as np
import random


# ---------- input variables ---------- 
min_output_size = 10000 # minimum output size in pixels - recommended values 5000 to 30000
min_cell_size = 25 # minimum size of each small image or cell in the output image in pixels - recommended 10 to 100
max_cell_size = 100 # maximum size of each small image or cell in the output image in pixels - recommended 40 to 400
n_inputs = 557 # number of inputs in the "inputs folder" - recommended 100 to 2000 - images with a variety of colors produce good results 
output_name = 'output.jpg' # name of the output image that is saved after creating the collage
target_name = 'target.jpg' # name of the image you want to replicate
inputs_name = 'input_images/input ({}).jpeg' # input_folder/input_number.format as explained in the comments at the beginning
create_reduced = True # set it to true if you don't have a variety of images with different sizes

print('\n# ---------- Selected configuration ---------- #')
print('output name:', output_name)
print('target name:', target_name)
print('inputs name:', inputs_name)
print('no. of inputs:', n_inputs)
print('minimum output size:', min_output_size)
print('cell size:', min_cell_size)
print('# -------------------------------------------- #\n')


# ---------- defining functions ----------
dissimilarity = lambda a, b: abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])
fits = lambda x, p: not np.any(filled[p[0]:p[0]+(x[0]//min_cell_size), p[1]:p[1]+(x[1]//min_cell_size)])
def reduced(a, b):
    if a>max_cell_size: d = max_cell_size/a; a, b = round(a*d), round(b*d)
    if b>max_cell_size: d = max_cell_size/b; a, b = round(a*d), round(b*d)
    if a<min_cell_size: d = min_cell_size/a; a, b = round(a*d), round(b*d)
    if b<min_cell_size: d = min_cell_size/b; a, b = round(a*d), round(b*d)
    return (a-a%min_cell_size, b-b%min_cell_size)
def misses(a, b):
    miss_count = 0
    for ai, bi in zip(a, b):
        for aj, bj in zip(ai, bi):
            if aj!=bj: miss_count += 1
    return miss_count


# ---------- loading images into numpy arrays ---------- 
print('Loading images... ', end='\r')
if n_inputs>5000: print('\nHigh memory requirement, reduce the \'n_inputs\' (number of inputs) or \'min_cell_size\' (cell size)'); exit(0)

try:
    inputs = [cv2.imread(inputs_name.format(i)) for i in range(1, n_inputs+1)]
    input_sizes = [reduced(inp.shape[0], inp.shape[1]) for inp in inputs]
    inputs = [cv2.resize(inputs[i], (input_sizes[i][1], input_sizes[i][0])) for i in range(n_inputs)]

    if create_reduced:
        for i in range(n_inputs):
            rf = min(input_sizes[i])/min_cell_size
            if rf==1: continue
            else:
                s = (math.ceil(input_sizes[i][0]*rf), math.ceil(input_sizes[i][1]*rf))
                s = (s[0]-s[0]%min_cell_size, s[1]-s[1]%min_cell_size)
                input_sizes.append(s); inputs.append(cv2.resize(inputs[i], (s[1], s[0])))
        n_inputs = len(input_sizes)

except Exception: print('Loading images... Error \nCheck the names in the input folder and modify the variable \'inputs_name\''); exit(0)

try:
    target_img = cv2.imread(target_name)
    output_size = (target_img.shape[0], target_img.shape[1])
    if output_size[0]<min_output_size: output_size = (min_output_size, output_size[1]*min_output_size//output_size[0])
    if output_size[1]<min_output_size: output_size = (output_size[0]*min_output_size//output_size[1], min_output_size)
    output_size = (output_size[0]-output_size[0]%min_cell_size, output_size[1]-output_size[1]%min_cell_size)
    n_cells = (output_size[0]//min_cell_size, output_size[1]//min_cell_size)
    target_img = cv2.resize(target_img, (n_cells[1], n_cells[0]))

    if output_size[0]>40000 or output_size[1]>40000: print('\nHigh memory requirement, reduce the \'min_output_size\' (minimum output size)'); exit(0)
    output = np.zeros((output_size[0], output_size[1], 3), dtype=np.uint8)
    filled = np.full(n_cells, 0, dtype=np.bool)

except Exception: print('Loading images... Error \nCheck the name of the target image and modify the variable \'target_name\''); exit(0)
print('Loading images... Done')


# ---------- calculating averages ---------- 
print('Calculating averages...', end='\r')
try:
    input_avgs = tuple(inp.mean(axis=(0,1)) for inp in inputs)
    target_avgs = cv2.resize(target_img, (n_cells[1], n_cells[0]))
except: print('Calculating averages... Error'); exit(0)
print('Calculating averages... Done')


# ---------- searching for optimal cells ----------
image_count = 0
for i in range(n_cells[0]):
    for j in range(n_cells[1]):
        if filled[i,j]: continue
        min_d, min_p = 99999, -1
        for k in range(n_inputs):
            if not fits(input_sizes[k], (i,j)): continue
            d = dissimilarity(target_avgs[i:i+input_sizes[k][0]//min_cell_size, j:j+input_sizes[k][1]//min_cell_size].mean(axis=(0,1)), input_avgs[k])
            if d<min_d: min_d, min_p = d, k
            if d==0 and random.randint(0,1)==1: break
        if min_p == -1: continue
        e = output_size[0]-i*min_cell_size, output_size[1]-j*min_cell_size
        output[i*min_cell_size:i*min_cell_size+input_sizes[min_p][0], j*min_cell_size:j*min_cell_size+input_sizes[min_p][1]] = inputs[min_p][:e[0], :e[1]]
        e = n_cells[0]-i, n_cells[1]-j
        filled[i:i+input_sizes[min_p][0]//min_cell_size, j:j+input_sizes[min_p][1]//min_cell_size] = np.full((input_sizes[min_p][0]//min_cell_size, input_sizes[min_p][1]//min_cell_size), True, dtype=np.bool)[:e[0], :e[1]]
        image_count += 1
    percent = (i+1)*100//n_cells[0]
    print('Search for opitmal cells - Progress: [%s%s] %d%%'%('-'*int(percent*0.2), ' '*(20-int(percent*0.2)), percent), end='\r')
print('\n')

# ---------- saving output image ----------
print('Saving image...', end='\r')
cv2.imwrite(output_name, output)
print('Saving image... Done')
print('Image saved as',output_name)
print('output shape:', output_size)
print('no. of images:', image_count,'\n')
