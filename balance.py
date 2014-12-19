number = [1,3,5,10,3,6]
sum1,sum0 = 0,0
for x in range(len(number)):
	sum0 = sum0+number[x]
	if x < len(number)-2:
		for y in range(len(number[x+2:])):
			sum1 = sum1 + number[x+2+y]
	if sum0==sum1:
		print number[x+1]
		break
	sum1=0
