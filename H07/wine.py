# make run input='input.txt' output='output.txt'
import sys

class kdnode:
    def __init__(self, input):
        self.left = None
        self.right = None
        self.dimension = None
        self.value = input[0]
        self.elements = input[1]

def addToTree(root, node):
    if (node[1][root.dimension] < root.elements[root.dimension]):
        if root.left == None:
            root.left = kdnode(node)
            root.left.dimension = (root.dimension + 1) % 11
        else:
            addToTree(root.left, node)
    else:
        if root.right == None:
            root.right = kdnode(node)
            root.right.dimension = (root.dimension + 1) % 11
        else:
            addToTree(root.right, node)

def closestNeighbor(root, node, min):
    if root == None:
        return min
    if (root.elements != node[1]):
        minToNode = (sum([(a - b) ** 2 for a, b in zip(min.elements, node[1])])) ** 0.5
        rootToNode = (sum([(a - b) ** 2 for a, b in zip(root.elements, node[1])])) ** 0.5
        if rootToNode < minToNode:
            min = root

    if (node[1][root.dimension] < root.elements[root.dimension]):
        min = closestNeighbor(root.left, node, min)
        # min = closestNeighbor(root.right, node, min)
    else:
        min = closestNeighbor(root.right, node, min)
        # min = closestNeighbor(root.left, node, min)
    return min

wine = open('wine.txt', "r")

line = next(wine)
elements = line.split(" ")

input = open(sys.argv[1], 'r')
k = int(next(input))

n = int(elements[0])
d = int(elements[1])

# print(str(n) + " " + str(d))
wines = []

for i in range(n):
    line = next(wine)
    elements = line.split(" ")
    label = float(elements[0])

    elements = [float(s) for s in elements[1:]]

    mean = sum(elements) / len(elements)
    elements = [x - mean for x in elements]

    stdev = (sum([x ** 2 for x in elements]) / len(elements)) ** 0.5
    elements = [x / stdev for x in elements]

    wines.append((label, elements))

pivot = wines[int(len(wines) / 2)]


root = kdnode(pivot)
root.dimension = 0

for i in range(int(len(wines) / 2) - 1, -1, -1):
    addToTree(root, wines[i])

for i in range(int(len(wines) / 2) + 1, len(wines)):
    addToTree(root, wines[i])

kclosest = []
for i in range(0, len(wines)):
    closest = closestNeighbor(root, wines[i], root)
    rating = (sum([(a - b) ** 2 for a, b in zip(closest.elements, wines[0][1])])) ** 0.5
    if not (any(map(lambda x: x[0] == rating, kclosest))):
        if len(kclosest) < k:
            kclosest.append((rating, ((closest.value, closest.elements), wines[i])))
        else:
            highestrating = max(kclosest, key=lambda x: x[0])
            if (rating < highestrating[0]):
                kclosest.remove(highestrating)
                kclosest.append((rating, ((closest.value, closest.elements), wines[i])))

# Showing the closest pairs
for i in range(len(kclosest)):
    print("Ranking: " + str(kclosest[i][0]))
    print("Node 1: " + str(kclosest[i][1][0]))
    print("Node 2: " + str(kclosest[i][1][1]) + "\n")

# Error
result = 0
for i in range(len(kclosest)):
    result += (kclosest[i][1][0][0] - kclosest[i][1][1][0]) ** 2

result /= n

print(result)