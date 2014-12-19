number=[1,2,2,3,4]
settmp = set(number)
dict = {}
for x in settmp:
	dict[str(x)]=0
for y in range(len(number)):
	dict[str(number[y])] = dict[str(number[y])]+1
list = [(x,dict[x])  for x in dict]
max = list[0][1]
for z in range(len(list)):
	if list[z][1]>max:
		index,max = z,list[z][1]
print "value=>", list[index][0]
listmp = []
for a in range(len(number)):
	if number[a] == int(list[index][0]):
		listmp.append(a)	
print 'position=>',listmp
