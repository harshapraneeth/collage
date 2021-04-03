# importing necessary libraires
import cv2
import numpy as np

# input variables
output_size, target_size, cell_size = 5000, 500, 50
output_name, target_name, input_name = 'rakul.jpg', 'target.jpg', 'input_images/input ({}).jpeg'
n_inputs = 500

n_cells = output_size//cell_size
target_cell_size = target_size//n_cells

# loading images into numpy arrays
inputs = tuple(cv2.resize(cv2.imread(input_name.format(i)), (cell_size, cell_size)) for i in range(1, n_inputs+1))
target = cv2.resize(cv2.imread(target_name), (target_size, target_size))
output = np.zeros((output_size, output_size, 3), dtype=np.uint8)

# define similarity measure
dissimilarity = lambda a, b: abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

# calculating measures
input_avgs = [ tuple(map(int, inp.mean(axis=(0,1)))) for inp in inputs ]
target_avgs = [
    [ tuple(map(int, target[i*target_cell_size:(i+1)*target_cell_size, j*target_cell_size:(j+1)*target_cell_size].mean(axis=(0,1))))  for j in range(n_cells) ] 
    for i in range(n_cells)
]

# searching for optimal cells
dis_table = dict()
for i in range(n_cells):
    for j in range(n_cells):
        try: min_p = dis_table[target_avgs[i][j]]
        except:
            min_d, min_p = dissimilarity(input_avgs[0], target_avgs[i][j]), 0
            for ii in range(1, n_inputs):
                d = dissimilarity(input_avgs[ii], target_avgs[i][j])
                if d==0: min_p=ii; break
                if d<min_d: min_d, min_p = d, ii
            dis_table[target_avgs[i][j]] = min_p
        for ii in range(cell_size):
            for jj in range(cell_size):
                output[i*cell_size+ii, j*cell_size+jj] = inputs[min_p][ii, jj]
    percent = (i+1)*100//n_cells
    print('Progress: [%s%s] %d%%'%('-'*int(percent*0.2), ' '*(20-int(percent*0.2)), percent), end='\r')

# save output image
cv2.imwrite(output_name, output)
print('\n\nImage saved as',output_name,'\n')
