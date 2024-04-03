fo = open("lab.py", "r")
print ("Name of the file: ", fo.name)
basket = []
for index in range(7):
	line = next(fo)
	print ("Line No %d - %s" % (index, line))
	basket.append("Line: %d\nContent: %s" % (index, line))
# Close opened file
fo.close()

print(basket)