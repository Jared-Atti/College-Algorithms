import sys
import heapq

alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

'''
This function is called by get_tokens function to process individual words.
A word could consist of many tokens. This function identifies individual
tokens from the beginning and end of words.
For example, the word ***Hobbit!! is broken into tokens *, *, *, Hobbit, ! and !.
This list of tokens is returned. Punctuations inbetween a word are ignored and treated as a single token.
This function is called by get_tokens.
'''
def process_word(word):
	frontlist = list()
	i = 0
	while i < len(word) and word[i] not in alphabets:
		frontlist = frontlist + list(word[i])
		i += 1
	
	endlist = list()
	start = i
	j = len(word) - 1
	while j >= i and word[j] not in alphabets:
		endlist = list(word[j])	+ endlist
		j -= 1

	wrd = ''
	if i <= j:
		wrd = word[i:j+1]
	
	wordlist = list()
	if frontlist != list():
		wordlist = wordlist + frontlist
	if wrd != '':
		wordlist = wordlist + [wrd]
	if endlist != list():
		wordlist= wordlist + endlist

	return wordlist

'''
Takes in a name of a file, and returns a list of tokens.
The list of tokens includes whitespaces (spaces, tabs and newlines) as separate tokens.
Makes use of process_word function.
'''
def get_tokens(filename):
	tokens = list()
	f = open(filename, 'r', encoding='utf-8')

	for line in f:
		line = line.split(' ')
		
		for word in line:
			if word == '':
				# Caution! Some empty strings '' from the split method should not be turned into spaces.
				tokens.extend([' '])
				continue

			wordlist = process_word(word)
			tokens.extend(wordlist)
			if wordlist[-1] != '\n':
				tokens.extend(list(' '))
			
	f.close()
	return tokens

'''
Converts a binary codestring into a bytearray.
This function is called by huffman_encode, which is called
by write_file_output.
'''
def binarystring_to_bytearray(codestring):
	return int(codestring, 2).to_bytes(len(codestring) // 8, byteorder = 'big')

'''
This function takes a codestring, adds extra 0 bits if the length of codestring is not divisble by 8,
then converts the codestring into a string of byte characters. The returned string includes the # extra bits
followed by the encoded string on the next line.
This function is called by write_file_output.
'''
def huffman_encode(codestring):
	
	# Find the number of extra 0 bits to add if codestring length is not a multiple of 8.
	extrabits = 8 - (len(codestring) % 8)
	extras = ''
	# Add 0s in the end.
	for i in range(extrabits):
		extras = extras + '0'
	codestring = codestring + extras

	# Encode the codestring 
	encode_bytearray = binarystring_to_bytearray(codestring)
	return encode_bytearray

'''
Takes the filename (without the .enc extension, the treestring which is the
	encoding of the Huffman tree, and codestring which is the binary string
	encoding of the text. This function converts the codestring into a byte array
	and writes everything into the output file. The output file is a byte file.
'''
def write_file_output(filename, treestring, codestring):
	encodestring = huffman_encode(codestring)
	treestring = treestring.encode('utf-8')
	# x = treestring.decode('utf-8')
	
	g = open(filename + ".enc", 'wb')
	g.write(treestring)
	g.write(encodestring)
	g.close()

# You can put your Huffman encoding algorithm here.

# Class for nodes in the tree
class Node:
	def __init__(self, token, frequency, left, right):
		self.token = token
		self.frequency = frequency
		self.left = left
		self.right = right

	def __lt__(self, other):
		return self.frequency < other.frequency

	def __gt__(self, other):
		return self.frequency > other.frequency

# A main function to run the desired functions
def main():
	# Creates treestring and codestring using the tokens found in the input file
	treestring, codestring = create_encoding_strings(get_tokens(sys.argv[-1]))
	# Calls write_file_output to produce final encoded file
	write_file_output(sys.argv[-1], treestring, codestring)

def makeMap(tree, path):
	left = {}
	right = {}
	# Checks for left child
	if tree.left is not None:
		left.update(makeMap(tree.left, ''.join([path, '0'])))
	# Checks for right child
	if tree.right is not None:
		right.update(makeMap(tree.right, ''.join([path, '1'])))
	# No Children, this is a leaf, add leaf to map
	if tree.left is None and tree.right is None:
		return {tree.token : path}
	return {**left, **right}

index = 1
def getLabels(tree):
	global index
	# Idx will hold { Index : (children) }
	thisIdx  = {}
	# Token will hold { Token : Index }
	thisToken  = {}
	# Checks for left child
	if tree.left is not None:
		left = getLabels(tree.left)
	# Checks for right child
	if tree.right is not None:
		right  = getLabels(tree.right)
	# Gets this node if it is not a leaf
	if tree.left is not None and tree.right is not None:
		thisIdx  = { index : (tree.left, tree.right) }
		thisToken = { tree.token : index }
		index += 1
	# No Children, this is a leaf, add leaf to map
	if tree.left is None and tree.right is None:
		return ({}, {})
	return {**left[0] , **right[0], **thisIdx }, {**left[1] , **right[1], **thisToken }

def create_encoding_strings(tokens):
	treestring = ''
	codestring = ''

	# print("get tokens finished")

	# Building the histogram of token frequencies
	histogram = {}
	for t in tokens:
		if t in histogram:
			histogram[t] += 1
		else:
			histogram[t] = 1

	# Inserting the histogram elements into a priority queue, converts dict into list of tuples with count being in front and a node being second, then uses heapify
	pq = [(count, Node(token, count, None, None)) for token, count in histogram.items()]
	heapq.heapify(pq)

	# print("priority queue created")

	# Build the Huffman tree as a binary tree
	while len(pq) > 1:
		x = heapq.heappop(pq)
		y = heapq.heappop(pq)
		combined = ''.join([x[1].token, y[1].token])
		t = Node(combined, x[1].frequency + y[1].frequency, x[1], y[1])
		pq.append((t.frequency, t))

	# Pops the last element from pq, the root of the tree
	tree = heapq.heappop(pq)[1]

	# print("tree created")

	# Maps the tokens by traversing the tree and getting the path for each leaf
	map = makeMap(tree, '')

	# print("map created")

	# Creates the codestring by converting the tokens to binary
	i = 0
	tempstring = ''
	for t in tokens:
		# codestring = ''.join([codestring, map[t]])
		tempstring = ''.join([tempstring, map[t]])
		i += 1
		if (i % 10000 == 0):
			codestring = ''.join([codestring, tempstring])
			tempstring = ''
	codestring = ''.join([codestring, tempstring])

	# print("codestring created")

	# Getting a list of the labels within the tree
	idxchildren, tokenidx = getLabels(tree)

	# print("label maps created")

	# Starting treestring with number of labels
	treestring = str(len(idxchildren)) + '\n'

	for node in idxchildren:
		children = idxchildren[node]
		# Left is a leaf
		if children[0].left is None and children[0].right is None:
			t = children[0].token
			if (t == '\r'):
				t = '~1'
			elif (t == ' '):
				t = '~2'
			elif (t == '\t'):
				t = '~3'
			elif (t == '\n'):
				t = '~4'
			treestring = ''.join([treestring, t])
		# Left is an internal
		else:
			treestring = ''.join([treestring, "#"])
			treestring = ''.join([treestring, str(tokenidx[children[0].token])])
		# Space between
		treestring = ''.join([treestring, " "])
		# Right is a leaf
		if children[1].left is None and children[1].right is None:
			t = children[1].token
			if (t == '\r'):
				t = '~1'
			elif (t == ' '):
				t = '~2'
			elif (t == '\t'):
				t = '~3'
			elif (t == '\n'):
				t = '~4'
			treestring = ''.join([treestring, t])
		# Right is an internal
		else:
			treestring = ''.join([treestring, "#"])
			treestring = ''.join([treestring, str(tokenidx[children[1].token])])
		treestring = ''.join([treestring, "\n"])

	# Adding extra bits if needed
	b = 8 - len(codestring) % 8
	# for i in range(b):
	# 	codestring = ''.join([codestring, '0'])
	treestring = ''.join([treestring, str(b) + '\n'])

	return treestring, codestring

# Runs main
main()
