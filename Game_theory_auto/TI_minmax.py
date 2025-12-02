import numpy as np
import copy
m=[]

for e in range(1,4):
    temp=[]
    for i in range(1,5):
        temp.append(10-2*e+3*i-e*i)
    m.append(copy.deepcopy(temp))
m=np.array(m)
print(m)