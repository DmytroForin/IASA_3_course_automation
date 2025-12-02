import numpy as np
import pandas as pd
import copy

def sys_transform(a, base):
    temp=0
    digits=[]
    while a>base-1:
        temp=a%base
        #a=a-temp
        a=a//base
        digits.append(temp)
    digits.append(a)
    res=""
    for i in reversed(range(len(digits))):
        res=res+str(digits[i])
    return res

gamers={'F','I'}
s=[['A','B'],['H','M']]
s1=copy.deepcopy(s[0])
s2=[]

def m(x,y):
    return (8*(x+1)+7*y)
def e1(x):
    return (3*((x+1)**2))
def e2(y):
    return (4*y)

#####
#####
#####
#TREE FORM


for i in range(len(s[0])):
    for j in range(len(s[1])):
        temp=m(i,j)
        w1=temp-e1(i)
        w2=temp-e2(j)
        print(f"{s[0][i]}{s[1][j]}: {(w1,w2)}")

# сделай кластерами
for i in range(len(s[1])**len(s[0])):
    s2.append(sys_transform(i,len(s[1])))
for i in range(len(s2)):
    while len(s2[i])<len(s[0]):
        s2[i]='0'+s2[i]
#print(s2)


for i in range(len(s2)):
    s2[i]=list(s2[i])
    #print(s2[i])
    for j in range(len(s2[i])):
        s2[i][j]=s[1][int(s2[i][j])]
    s2[i]="".join(s2[i])
    #print(s2[i])
    
#print(s2)

dict={}
for i in range(len(s1)):
    dict.update({str(s1[i]): np.zeros(len(s2))})
norm_form=pd.DataFrame(dict,index=s2, dtype=object)
#print(norm_form)



for i in norm_form.columns:
    for j in norm_form.index:
        temp=m(s[0].index(i),s[1].index(j[s[0].index(i)]))
        w1=temp-e1(s[0].index(i))
        w2=temp-e2(s[1].index(j[s[0].index(i)]))
        norm_form.at[j,i]=np.array([w1,w2])
print(norm_form.T)


'''
print(m(0,0))
print(e1(0,0))
print(e2(0,0))
'''