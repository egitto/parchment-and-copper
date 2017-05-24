#!/usr/bin/python
from fractions import Fraction as Fract

def divide_estate(estate,creditors):
	if not creditors == sorted(creditors): print("creditors must be in ascending order"); return []
	n = len(creditors)
	paid = [0] * n
	creditors.reverse()
	for i in range(n,0,-1):
		half_owed = [0]+[o/2 - p for o,p in zip(creditors,paid)]
		payment = min(estate/(i),half_owed[i])
		for j in range(i):
			paid[j] += payment
			estate -= payment
	for i in range(n):
		loss = [c - p for c, p in zip(creditors,paid)]+[0]
		payment = min(estate/(i+1),loss[i]-loss[i+1])
		for j in range(i+1):
			paid[j] += payment
			estate -= payment
	creditors.reverse()
	paid.reverse()
	return paid

def divide_estate_test():
	tests = [[[150,[100,200,300]],[50,50,50]]]
	tests += [[[200,[100,200,300]],[50,75,75]]]
	tests += [[[300,[100,200,300]],[50,100,150]]]
	tests += [[[400,[100,200,300]],[50,125,225]]]
	tests += [[[600,[100,200,300]],[100,200,300]]]
	for i in tests:
		actual = divide_estate(*i[0]) 
		expected = i[1]
		assert actual == expected, print("expected",expected,"\nactual",actual) 

estate = Fract(input("Enter estate to split: "))
c_string = input("Enter sorted list of creditors: ").replace(","," ").replace("  "," ")
creditors = [Fract(i) for i in c_string.split()]
paid = [float(i) for i in divide_estate(estate,creditors)]
print("Distribution of funds: ",*paid)