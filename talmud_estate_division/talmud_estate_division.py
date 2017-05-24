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

if __name__ == '__main__':
	import sys, re
	def print_help(): 
		s = ['no arguments: prints help string',
		'\n-f: total estate funds to allocate',
		'\n-c: sorted comma-separated list of debts',
		'\nusage example:',
		'\n   talmud_estate_division.py -f 200 -c 100,200,300']
		print(*s)
	creditors = estate = None
	prev_arg = ''
	for i in sys.argv[1:]:
		if prev_arg == '-f':
			if re.fullmatch('\d+(\.\d*)?',i):
				estate = Fract(i)
		elif prev_arg == '-c':
			if re.fullmatch('(\d+(\.\d*)?,)*\d+(\.\d*)?',i):
				creditors = [Fract(j) for j in i.split(',')]
		prev_arg = i
	if creditors and estate: print(str([float(i) for i in divide_estate(estate,creditors)])[1:-1])
	else: print_help()