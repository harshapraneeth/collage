# importing necessary libraires

from PIL import Image
import math
import numpy as np

# input variables

cell_size = 100
output_size = 10000
target_name = 'target.jpg'
input_name = 'input_images2/input ({}).jpg'
output_name = 'friends.jpg'
n_inputs = 380
input_rr = 25

n_cells = output_size//cell_size
target_size = output_size//input_rr
target_cell_size = cell_size//input_rr

# loading images into numpy arrays

inputs = np.array(
    [ Image.open(input_name.format(i)).resize((cell_size, cell_size)).getdata() for i in range(1, n_inputs+1) ],
    dtype=np.uint8
).reshape(n_inputs, cell_size, cell_size, 3)

target = np.array(
    Image.open(target_name).resize((target_size, target_size)).getdata(),
    dtype=np.uint8
).reshape(target_size, target_size, 3)

output = np.full((output_size, output_size, 3), 0, dtype=np.uint8)

# define functions

mean_color = lambda A, x, y, size, n: tuple(sum(A[i][j][k] for i in range(x, x+size) for j in range(y, y+size))//n for k in range(3))
distance = lambda n, p1, p2: math.sqrt(sum((p1[i]-p2[i])**2 for i in range(n)))
similarity = lambda a, b: 45000//(1+distance(3, a, b))

def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

# calculating measures

n_c, n_t_c = cell_size*cell_size, target_cell_size*target_cell_size

input_avgs = [ mean_color(inp, 0, 0, cell_size, n_c) for inp in inputs ]

target_avgs = [
    [ mean_color(target, i*target_cell_size, j*target_cell_size, target_cell_size, n_t_c) for j in range(n_cells) ]
    for i in range(n_cells)
]

# searching for optimal cells

dis_table = dict()

for i in range(n_cells):
    for j in range(n_cells):

        try: max_p = dis_table[target_avgs[i][j]]
        
        except:
            max_sim, max_p = similarity(input_avgs[0], target_avgs[i][j]), 0
            for ii in range(1, n_inputs):
                sim = similarity(input_avgs[ii], target_avgs[i][j])
                if sim>max_sim: max_sim, max_p = sim, ii
            dis_table[target_avgs[i][j]] = max_p

        for ii in range(cell_size):
            for jj in range(cell_size):
                output[i*cell_size+ii, j*cell_size+jj] = inputs[max_p][ii, jj]

    progressBar((i+1)*100/n_cells,100, 25)

output_image = Image.fromarray(output)
output_image.save(output_name)
print('\n\nImage saved as',output_name,'\n')

