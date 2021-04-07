# importing necessary libraires
import cv2
import numpy as np

# input variables
output_size, cell_size, n_inputs = 5000, 50, 570
output_name, target_name, input_name = 'rakul.jpg', 'target.jpg', 'input_images/input ({}).jpeg'
n_cells = output_size//cell_size

# loading images into numpy arrays
print('Loading images...',end='\r')
inputs = tuple(cv2.resize(cv2.imread(input_name.format(i)), (cell_size, cell_size)) for i in range(1, n_inputs+1))
target = cv2.resize(cv2.imread(target_name), (output_size, output_size))
print('Loading images... Done')

# define similarity measure
dissimilarity = lambda a, b: abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

# calculating measures
print('Calculating averages...',end='\r')
input_avgs = [ tuple(map(int, inp.mean(axis=(0,1)))) for inp in inputs ]
target_avgs = [
    [ tuple(map(int, target[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size].mean(axis=(0,1))))  for j in range(n_cells) ] 
    for i in range(n_cells)
]
print('Calculating averages... Done')

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
        target[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size] = inputs[min_p]
    percent = (i+1)*100//n_cells
    print('Search for opitmal cells - Progress: [%s%s] %d%%'%('-'*int(percent*0.2), ' '*(20-int(percent*0.2)), percent), end='\r')

# save output image
cv2.imwrite(output_name, target)
print('\n\nImage saved as',output_name,'\n')
