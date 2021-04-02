# %% importing necessary libraires
from PIL import Image
import random
import math
import numpy as np
from IPython.display import clear_output

# %% input variables

cell_size = 40
output_size = 10000
target_name = 'target.jpg'
input_name = 'input_images/input ({}).jpeg'
n_inputs = 570
input_rr = 20

n_cells = output_size//cell_size
target_size = output_size//input_rr
target_cell_size = cell_size//input_rr

# %% loading images into numpy arrays
%%time

inputs = np.array(
    [
        Image.open(input_name.format(i))
        .resize((cell_size, cell_size))
        .getdata()

        for i in range(1, n_inputs+1)
    ],
    dtype=np.uint8
).reshape(n_inputs, cell_size, cell_size, 3)

target = np.array(
    Image.open(target_name).resize((target_size, target_size)).getdata(),
    dtype=np.uint8
).reshape(target_size, target_size, 3)

output = np.full((output_size, output_size, 3), 0, dtype=np.uint8)

print('inputs shape:', inputs.shape)
print('target shape:', target.shape)
print('output shape:', output.shape)

# %% define functions

def color_counts(arr, x, y, size):
    counts = dict()
    for i in range(x, x+size):
        for j in range(y, y+size):
            try: counts[tuple(arr[i, j])] += 1
            except: counts[tuple(arr[i, j])] = 1
    return counts
    
def mode_color(arr, x, y, size):
    counts = color_counts(arr, x, y, size)
    max_color, max_count = None, -1
    for color in counts.keys():
        if counts[color]>max_count: max_color, max_count = color, counts[color]
    return max_color

def avg_color(arr, x, y, size):
    r, g, b, n = 0, 0, 0, size*size
    for i in range(x, x+size):
        for j in range(y, y+size):
            c = arr[i,j]
            r, g, b = r+c[0], g+c[1], b+c[2]
    return (r//n, g//n, b//n)

distance = lambda n, p1, p2: math.sqrt(sum((p1[i]-p2[i])**2 for i in range(n)))

def dissimilarity(A_mode, A_avg, B_mode, B_avg):
    c_mode, c_avg= 1, 1
    return c_mode*distance(3, A_mode, B_mode) + c_avg*distance(3, A_avg, B_avg)

# %% calculating measures
%%time

input_modes = [
    mode_color(inp, 0, 0, cell_size)
    for inp in inputs
]

input_avgs = [
    avg_color(inp, 0, 0, cell_size)
    for inp in inputs
]

target_modes = [
    [
        mode_color(target, i*target_cell_size, j*target_cell_size, target_cell_size)
        for j in range(n_cells)
    ]
    for i in range(n_cells)
]

target_avgs = [
    [
        avg_color(target, i*target_cell_size, j*target_cell_size, target_cell_size)
        for j in range(n_cells)
    ]
    for i in range(n_cells)
]

# %% searching for optimal cells
%%time

dis_table = dict()

for i in range(n_cells):
    for j in range(n_cells):
        cell_mode, cell_avg = target_modes[i][j], target_avgs[i][j]
        try: min_p = dis_table[(cell_avg, cell_mode)]; print('found')
        except:
            min_dissim, min_p = dissimilarity(input_modes[0], input_avgs[0], cell_mode, cell_avg), 0
            for ii in range(1, n_inputs):
                sim = dissimilarity(input_modes[ii], input_avgs[ii], cell_mode, cell_avg)
                if sim<min_dissim: min_dissim, min_p = sim, ii
            dis_table[(cell_avg, cell_mode)] = min_p
        for ii in range(cell_size):
            for jj in range(cell_size):
                output[i*cell_size+ii, j*cell_size+jj] = inputs[min_p][ii, jj]
    clear_output()
    print('completed:', (i+1)*100/n_cells, '%')

output_image = Image.fromarray(output)
output_image.save('output_avg.jpeg')

