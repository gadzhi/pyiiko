from itertools import groupby
def test(a):
	return[it for it , _ in groupby(a, lambda x: x[0])]

tes = [1,1,2,2,4,4,1,1]
print(test(tes))