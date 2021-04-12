import numpy as np
import random

minh, maxh = 1, 10
minw, maxw = 1, 10
n_shapes = 100
box_shape = 1920, 1080  

sizes = sorted(tuple((random.randint(minw, maxw)*10, random.randint(minh, maxh)*10) for _ in range(n_shapes)), reverse=True)
min_fill, max_fill = (0,0), (0,0)
stack = []

def add(x, p):
    global min_fill, max_fill, stack
    min_fill = (min(min_fill[0], p[0]), min(min_fill[1], p[1]))
    max_fill = (max(max_fill[0], p[0]+sizes[x][0]), max(max_fill[1], p[1]+sizes[x][1]))
    stack.append((x, p))

def fill(x): pass


add(0, (0,0))
while len(stack)>0: fill(stack[-1]); stack=stack[:-1]