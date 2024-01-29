# make run-chocolates input='chocolates.in1' output='output.txt'
import sys

class Spot(object):
    def __init__(self, id):
        self.id = id
        self.edges = {}
        self.travel_costs = {}

def traverse(spot1, spot2, spots):
    if spot1.id == spot2.id:
        return 0
    
    if spot1.id in spot2.travel_costs:
        spot2.travel_costs[spot1.id]
    
    if spot2.id in spot1.edges:
        return spot1.edges[spot2.id]
    
    traversals = []
    for edge in spot1.edges:
        traversals.append(spot1.edges[edge] + traverse(spots[edge], spot2, spots))
    return min(traversals)

input = open(sys.argv[1], 'r', encoding='utf-8')

line = next(input)
elements = line.split(" ")
n = int(elements[0])
p = int(elements[1])
c = int(elements[2])

child_spots = {}
for i in range(n):
    line = int(next(input))
    if line in child_spots:
        child_spots[line] += 1
    else:
        child_spots[line] = 1

spots = {}
for i in range(1, p + 1):
    spots[i] = Spot(i)
    if i not in child_spots:
        child_spots[i] = 0

for i in range(c):
    line = next(input)
    elements = line.split(" ")
    spot1 = int(elements[0])
    spot2 = int(elements[1])
    edge = int(elements[2])
    spots[spot1].edges[spot2] = edge
    spots[spot2].edges[spot1] = edge

for i in range(1, p + 1):
    for j in range(1, p + 1):
        spots[i].travel_costs[j] = traverse(spots[i], spots[j], spots)

min_cost = 9999999
for i in range(1, p + 1):
    spot_cost = 0
    for j in range(1, p + 1):
        spot_cost += spots[i].travel_costs[j] * child_spots[j]
    min_cost = min(min_cost, spot_cost)

print(min_cost)