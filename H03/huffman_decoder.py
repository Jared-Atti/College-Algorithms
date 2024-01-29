'''
This is a Huffman Decoder. The file has to be formatted correctly from the Huffman Encoder.
Please refer to the handout for the Huffman Encoder and its output format.

This program accepts a filename as input (without the .enc extension).
A file name with a .enc extension stands for a file that has been run through the Huffman Encoder
and has been compressed. This format includes an encoding of the Huffman tree.
A file name with a .dec extension stands for a file that been run through the Huffman Decoder.
This file should be equivalent to the original file.

Therefore the output of this program is stored in filename.dec
'''

import sys

'''
This class represents a Huffman tree node.
'''
class treenode:

	def __init__(self, label, left, right):
		self.label = label
		self.left = left
		self.right = right

'''
Converts a bytearray in string into a bitstring. Also removes extrabits (zeros)
	from the end.
'''
def bytearray_to_bitstring(string, extrabits):
	bytelist = ["{0:08b}".format(x) for x in string]
	retstring = ''.join(bytelist)
	return retstring[:-extrabits]

'''
Checks if a treenode tn is a leaf or not.
'''
def is_leaf(tn):
	if tn.left == None and tn.right == None:
		return True
	return False

'''
This function takes in the encoded binary string (codestring) and the root
node of the corresponding Huffman tree, and returns the decoded string.
Assumes that the root is not a leaf.
'''
def decode(codestring, root):
	tokenslist = list()
	cur = root
	for x in codestring:
		if x == '0':
			cur = cur.left
		elif x == '1':
			cur = cur.right
		else:
			print("codestring contains non-binary data. exiting application.")
			sys.exit(1)

		if is_leaf(cur):
			tokenslist.append(cur.label)
			cur = root

	return "".join(tokenslist)

# Whitespaces are represented differently. See handout.
whitespaces_map = {'~1': '', '~2': ' ', '~3': '\t', '~4': '\n'}

# The argument to the main program is the name of the encoded file (without the .enc extension)
if __name__ == "__main__":
	
	# Read the file and store lines in a list
	filename = sys.argv[1]
	h = open(filename + ".enc", 'rb')
	line = h.readline()
	
	tn_count = int(line)
	lines = list()
	for i in range(tn_count):
		line = h.readline().decode('utf-8')
		lines.append(line)
	line = h.readline()
	extrabits = int(line)
	encstring = h.read()
	h.close()
	
	# Create the Huffman tree
	node_map = dict()
	node_cnt = 0
	for i in range(tn_count):
		line = lines[i].split(' ')
		left = line[0]
		right = line[1].rstrip()
		
		if left not in node_map:
			if left in whitespaces_map:
				left = whitespaces_map[left]
			tnleft = treenode(left, None, None)
			node_map[left] = tnleft
		else:
			tnleft = node_map[left]
		
		if right not in node_map:
			if right in whitespaces_map:
				right = whitespaces_map[right]
			tnright = treenode(right, None, None)
			node_map[right] = tnright
		else:
			tnright = node_map[right]
		
		node_cnt += 1
		tnlabel = '#' + str(node_cnt)
		tn = treenode(tnlabel, tnleft, tnright)
		node_map[tnlabel] = tn
	
	root = node_map['#' + str(node_cnt)]
	
	# decode the encoded string
	decodestring = bytearray_to_bitstring(encstring, extrabits)
	decodestring = decode(decodestring, root)

	h = open(filename + ".dec", 'w', encoding='utf-8')
	h.write(decodestring)
	h.close()

