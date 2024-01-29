import sys
import os

filename = sys.argv[1]
s1 = os.stat(filename).st_size
s2 = os.stat(filename + ".enc").st_size


res = os.system("diff " + filename + ' ' + filename + ".dec > out")
if res == 0:
	print("decoded successfully.... same file as the original text, Yay!")
else:
	print("decoding failed. exiting application.")
	os.system("rm out")
	sys.exit(1)
os.system("rm out")

compression_ratio = s1 / s2
space_saving = 1 - s2 / s1

print("\n{:<40} {:>10}".format(filename, s1))
print("{:<40} {:>10}".format(filename + ".enc", s2))
print("{:<40} {:>10}".format("compression ratio achieved: ", str(round(compression_ratio, 3)) + ':1'))
print("{:<40} {:>10}".format("space saved: ", str(round(space_saving, 4) * 100) + '%'))
