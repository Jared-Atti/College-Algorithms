# Assignment 01: Joy with Parsing
# Jared Atti

# Imports sys to read file
import sys
with open(sys.argv[1], 'r') as f:
    contents = f.read()

contents = contents.split("\n")

# Index for navigating through contents
index = 0

# Reads first two integers
x = int(contents[index].split(" ")[0])
y = int(contents[index].split(" ")[1])
index += 1

# Initializing lists to store the nonterminals and terminals
nonterminals = [""] * x
terminals = [""] * y

# Reading the nonterminals into their list
for i in range(x):
    nonterminals[i] = contents[i + index] # index of nonterminals ranges from 1 through (1 + x) within contents
index += x

# Reading the terminals into their list
for i in range(y):
    terminals[i] = contents[i + index] # index of nonterminals ranges from (1 + x) through (1 + x + y) within contents
index += y

# Read the next value which should be an integer representing number of productions
p = int(contents[index])
index += 1

# Creating two lists of size p to store the left and right sides of each production
left = [""] * p
right = [""] * p

# Reads through the productions and fills left & right lists
for i in range(p):
    left[i] = contents[index]
    right[i] = contents[index + 1]
    index += 2

# Creates the productions list by zipping left and right
# productions = list(zip(left, right))
productions = {}
for i in range(len(left)):
    if left[i] not in productions:
        productions[left[i]] = []
    productions[left[i]].append(right[i])

# With productions now created, open input file to check validity
with open(sys.argv[2], 'r') as f:
    input = f.read()

# Recursive function for parsing a string, returns either true (valid) or false (invalid)
def parser(x, y, i, j):
    if x == y:
        return True
    if i >= len(x) or i >= len(y):
        return False
    if y[j] in terminals:
        if y[j] == x[i]:
            return parser(x, y, i + 1, j + 1)
        return False
    if y[j] in nonterminals:
        if y[j] in productions:
            for value in productions[y[j]]:
                newprod = y[:j] + value.split(" ") + y[j+1:]
                if "" in newprod:
                    newprod.remove('')
                if parser(x, newprod, i, j) == True:
                    return True
    return False

# Replace tabs and newlines with spaces in input
for x in range(len(input)):
    if input[x] == "\n" or input[x] == "\t":
        input = input[:x] + " " + input[x + 1:]

# Splits the input by spaces and removes and empty quotations that may have been created
fixedinput = []
input = input.split(" ")
for x in range(len(input)):
    if input[x] != "":
        fixedinput.append(input[x])

# Print statements for checking the input values
# print("Fixed Input: ", fixedinput)
# print("")
# print("Non-Terminals: ", nonterminals)
# print("Terminals: ", terminals)
# print("Productions: ", productions)

# Creates valid, a true/false variable depending on the result of parser
# parser is called with the list of input symbols, the starting production string, and the starting positions 0 and 0
first_element = next(iter(productions.items()))
valid = parser(fixedinput, [first_element[0]], 0, 0)

# Prints Results depending on validity
if valid:
    print("string is valid")
else:
    print("string is invalid")
