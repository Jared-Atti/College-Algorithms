def polyhash(line, x, m):
	hashsum = 0

	for i in range(len(line)):
		hashsum = (hashsum * x + ord(line[i])) % m
	return hashsum

m = 2 ** 63 # use this value of m for the hyperloglog.
x = 171043 

while True:
	inp = input()
	inp.strip()
	if inp == "stop":
		break
	ind = polyhash(inp, x, m)
	print(inp, ind)

# call the polyhash function with m = 2 ** 63 for hyperloglog.

# call the polyhash function with m = 2800 for count-min sketch

# x is the point at which we evaluate the hash function.

