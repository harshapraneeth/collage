# To use this program you need atleast 100 input images named 'input (0).jpg', 'input (1).jpg', and so on in a folder names input_images. 
# Or you can name the folder whatever you want and change the variable 'inputs_name' accordingly.
# You can rename all images in this pattern using "select all" and "rename". Select all images in the folder and rename them as "input".
# They will all be renamed as in the above pattern. Make sure they all are in the same format like jpeg, jpg or png. Also enter the correct format in the "inputs_name".

# The inputs folder should be in the same directory as the program itself or you can provide the full path of the input folder in the variable inputs_name.
# The target_name is the name of the image you want to produce from the smaller images and it should be in the same directory as the program. 
# Once you have all the images double click the 'run.bat' file. Or you can run the program from the terminal.


# ---------- importing necessary libraires ---------- 
import cv2
import numpy as np
import random


# ---------- input variables ---------- 
min_output_size = 10000 # minimum output size in pixels - recommended values [5000, 30000]
cell_size = (100, 100) # size of each small image (height, width) or cell in the output image in pixels - recommended [50, 300] (1/100th of the min_output_size)
n_inputs = 500 # number of inputs in the "inputs folder" - recommended 100 to 2000 - images with a variety of colors produce good results 
output_name = 'output.jpg' # name of the output image that is saved after creating the collage
target_name = 'target.jpg' # name of the image you want to replicate
inputs_name = 'input_images/input ({}).jpeg' # input_folder/input_number.format as explained in the comments at the beginning

print('\n# ---------- Selected configuration ---------- #')
print('output name:', output_name)
print('target name:', target_name)
print('inputs name:', inputs_name)
print('no. of inputs:', n_inputs)
print('minimum output size:', min_output_size)
print('cell size:', cell_size)
print('# -------------------------------------------- #\n')


# ---------- defining functions ----------
dissimilarity = lambda a, b: abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])


# ---------- loading images into numpy arrays ---------- 
print('Loading images... ', end='\r')
if n_inputs>5000: print('\nHigh memory requirement, reduce the \'n_inputs\' (number of inputs) or \'cell_size\' (cell size)min_cell_size'); exit(0)

try: inputs = tuple(cv2.resize(cv2.imread(inputs_name.format(i)), (cell_size[1], cell_size[0])) for i in range(1, n_inputs+1))
except Exception: print('Loading images... Error \nCheck the names in the input folder and modify the variable \'inputs_name\''); exit(0)

try:
    target_img = cv2.imread(target_name)
    output_size = (target_img.shape[0], target_img.shape[1])
    if output_size[0]<min_output_size: output_size = (min_output_size, output_size[1]*min_output_size//output_size[0])
    if output_size[1]<min_output_size: output_size = (output_size[0]*min_output_size//output_size[1], min_output_size)
    output_size = (output_size[0]-output_size[0]%cell_size[0], output_size[1]-output_size[1]%cell_size[1])
    n_cells = (output_size[0]//cell_size[0], output_size[1]//cell_size[1])
    target_img = cv2.resize(target_img, (n_cells[1], n_cells[0]))

    if output_size[0]>30000 or output_size[1]>30000: print('\nHigh memory requirement, reduce the \'min_output_size\' (minimum output size)'); exit(0)
    output = np.zeros((output_size[0], output_size[1], 3), dtype=np.uint8)

except Exception: print('Loading images... Error \nCheck the name of the target image and modify the variable \'target_name\''); exit(0)
print('Loading images... Done')


# ---------- calculating averages ---------- 
print('Calculating averages...', end='\r')
try:
    input_avgs = tuple( tuple( map(round,inp.mean(axis=(0,1))) ) for inp in inputs)
    target_avgs = tuple( tuple( tuple( map(round, target_img[i,j]) ) for j in range(n_cells[1]) ) for i in range(n_cells[0]) )
except: print('Calculating averages... Error'); exit(0)
print('Calculating averages... Done')


# ---------- searching for optimal cells ----------
dis_table = dict()
for i in range(n_cells[0]):
    percent = i*100//n_cells[0]
    print('Searching for opitmal cells - Progress: [%s%s] %d%%'%('-'*int(percent*0.2), ' '*(20-int(percent*0.2)), percent), end='\r')
    for j in range(n_cells[1]):
        try: min_p = dis_table[target_avgs[i][j]]
        except:
            min_d, min_p = dissimilarity(input_avgs[0], target_avgs[i][j]), 0
            for ii in range(1, n_inputs):
                d = dissimilarity(input_avgs[ii], target_avgs[i][j])
                if d==0 and random.randint(0,1)==0: min_p=ii; break
                if d<min_d: min_d, min_p = d, ii
            dis_table[target_avgs[i][j]] = min_p
        output[i*cell_size[0]:(i+1)*cell_size[0], j*cell_size[1]:(j+1)*cell_size[1]] = inputs[min_p]
print('Searching for opitmal cells - Progress: [%s] 100%%'%('-'*20),'\n')


# ---------- saving output image ----------
print('Saving image...', end='\r')
cv2.imwrite(output_name, output)
print('Saving image... Done')
print('Image saved as',output_name)
print('output shape:', output_size)
print('no. of cells:', n_cells)
print()