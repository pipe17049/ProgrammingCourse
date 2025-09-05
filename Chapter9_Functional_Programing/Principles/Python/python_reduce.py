
from functools import reduce

def my_sum(l,accum):
    if len(l)==0:
        return accum
    else:
        return my_sum(l[1:],accum+l[0])
    
l = [1,2,3,4,5,6]
print(my_sum(l,0))


print(reduce(lambda x, y: x*y, [2,4,5]))

info = ["Eduardo","Arias","321252888"]


print(reduce(lambda x, y: x+"-"+y, info))


