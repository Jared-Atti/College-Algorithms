# make run-concom input='concom.in1' output='output.txt'
import sys

class Company(object):
    def __init__(self, id):
        self.id = id
        self.owns = {}

checked = {}
partial = {}

def controls(c1, c2, companies):
    if (c1.id == 34 and c2.id == 1):
        None
    # Checks if the two companies are the same
    if (c1.id == c2.id):
        return False

    # Checks if c2 is an immediate child of c1 and the percentage is above 50
    if (c2.id in c1.owns and c1.owns[c2.id] > 50):
        return True
    
    # Starts a recursive loop to check all children of c1 to find ownership of c2
    global partial
    global checked
    partial = {}
    checked = {}
    # partial = c1.owns.copy()
    result = deepcontrols(c1, c2, companies)
    
    # If recursive loop result is above 50, c1 owns c2 through its children
    # if (result > 50 or (c2.id in partial and partial[c2.id] > 50)):
    if (c2.id in partial and partial[c2.id] > 50):
        return True

    # Returns false if c1 does not control c2
    return False

def deepcontrols(c1, c2, companies):
    global checked
    global partial
    # Checks c1 has not been checked yet
    if (c1.id in checked):
        return 0
    
    # Adds c1 to the checked map to avoid infinite looping
    checked[c1.id] = True
    
    # c1 is c2, no addition needed
    if (c1.id == c2.id):
        return 0
    

    # partial = {}
    # for firstchild in c1.owns:
    #     if c1.owns[firstchild] > 50:
    #         for grandchild in companies[firstchild].owns:
    #             if grandchild in partial:
    #                 partial[grandchild] += companies[firstchild].owns[grandchild]
    #             else:
    #                 partial[grandchild] = companies[firstchild].owns[grandchild]

    for child in c1.owns:
        # if c1.owns[child] > 50:
        if child in partial:
            partial[child] += c1.owns[child]
        else:
            partial[child] = c1.owns[child]

    result = 0

    # for piece in partial:
    #     if partial[piece] > 50 and piece in c1.owns and companies[piece].id == c2.id:
    #         return 1000
    
    # Checks every c1 child company
    for child in c1.owns:
        # Child company is desired company
        # if (companies[child].id == c2.id):
            # Returns percentage of ownership
            # return c1.owns[child]
        
        # if c1.owns[child] > 50:
        if child in partial and partial[child] > 50:
        # Child is not desired company, must check child's owned children
            # result += deepcontrols(companies[child], c2, companies)
            deepcontrols(companies[child], c2, companies)

    return result

input = open(sys.argv[1], 'r', encoding='utf-8')

num_ownerships = int(next(input))

companies = {}

for i in range(num_ownerships):
    line = next(input)
    elements = line.split(" ")
    owner_id = int(elements[0])
    controlled_id = int(elements[1])
    percentage = int(elements[2])

    if owner_id not in companies:
        companies[owner_id] = Company(owner_id)
    companies[owner_id].owns[controlled_id] = percentage

    if controlled_id not in companies:
        companies[controlled_id] = Company(controlled_id)

controllers = {}
for i in range(1, len(companies) + 1):
    for j in range(1, len(companies) + 1):
        if controls(companies[i], companies[j], companies):
            if i in controllers:
                controllers[i].append(j)
            else:
                controllers[i] = [j]

for i in controllers:
    for j in controllers[i]:
        print(str(i) + " " + str(j))
