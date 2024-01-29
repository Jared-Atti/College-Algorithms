import sys

class Node:
    def __init__(self, value):
        self.next = []
        self.pred = {}
        self.value = value

def fordfulkerson(source, sink):
    maxflow = 0

    for sourcetomatch in source.next:
        # min_edge2 = 4000
        # min_edge3 = 4000
        # min_edge1 = min(4000, sourcetomatch[1])
        for matchtoteam in sourcetomatch[0].next:
            # min_edge1 = min(4000, sourcetomatch[1])
            # min_edge2 = min(min_edge1, matchtoteam[1])
            for teamtosink in matchtoteam[0].next:
                min_edge1 = min(4000, sourcetomatch[1])
                min_edge2 = min(min_edge1, matchtoteam[1])
                min_edge3 = min(min_edge2, teamtosink[1])
                sourcetomatch = (sourcetomatch[0], sourcetomatch[1] - min_edge3)
                matchtoteam = (matchtoteam[0], matchtoteam[1] - min_edge3)
                teamtosink = (teamtosink[0], teamtosink[1] - min_edge3)
                sink.pred[matchtoteam[0]] += min_edge3
                matchtoteam[0].pred[sourcetomatch[0]] += min_edge3
                sourcetomatch[0].pred[source] += min_edge3
                maxflow += min_edge3

    return maxflow


input = open(sys.argv[1], 'r')

# Counts the number of teams in the input
num_teams = int(next(input))

# Map for the teams and their index in the scores list
teams = {}

# List for the scores of a team
scores = []
index = 0
top_score = 0

# Fills the maps with each team and their score
for i in range(num_teams):
    name = next(input)
    score = int(next(input))
    scores.append(score)
    teams[name] = index
    index += 1
    top_score = max(top_score, score)

# Counts the number of matches left to play
num_matches = int(next(input))

# List to hold the remaining matches
matches = []

# Holds the match indeces for each team
team_matches = {}
index = 0

# Creating a list of all the remaining matches
for i in range(num_matches):
    team1 = next(input)
    team2 = next(input)
    matches.append((team1, team2))

    if team1 in team_matches:
        team_matches[team1].append(index)
    else:
        team_matches[team1] = [index]
    
    if team2 in team_matches:
        team_matches[team2].append(index)
    else:
        team_matches[team2] = [index]
    index += 1

challenging_teams = []
elimated_teams = []
lowflow_teams = []

for zteam in teams:
    total_points = scores[teams[zteam]] + 3 * len(team_matches[zteam])

    if total_points < top_score:
        elimated_teams.append((zteam, scores[teams[zteam]]))
    else:
        source = Node(None)
        match_nodes = {}
        for match in matches:
            if zteam not in match:
                node = Node(match)
                match_nodes[node] = node
                source.next.append((node, 3))
                node.pred[source] = 0
        
        team_nodes = {}
        for m in match_nodes:
            mnode = match_nodes[m]
            team1 = mnode.value[0]
            team2 = mnode.value[1]
            if team1 not in team_nodes:
                node = Node(team1)
                team_nodes[team1] = node
            mnode.next.append((team_nodes[team1], 4000))
            team_nodes[team1].pred[mnode] = 0
            
            if team2 not in team_nodes:
                node = Node(team2)
                team_nodes[team2] = node
            mnode.next.append((team_nodes[team2], 4000))
            team_nodes[team2].pred[mnode] = 0

        sink = Node(None)
        for t in team_nodes:
            tnode = team_nodes[t]
            xpoints = scores[teams[tnode.value]] + 3 * len(team_matches[tnode.value])
            while total_points - 3 <= xpoints:
                xpoints -= 3
            xpoints -= scores[teams[tnode.value]]
            xpoints /= 3
            tnode.next.append((sink, int(xpoints)))
            sink.pred[tnode] = 0

        maxflow = fordfulkerson(source, sink)
        zpoints = 3 * (len(matches) - len(team_matches[zteam]))

        if maxflow == zpoints:
            challenging_teams.append((zteam, scores[teams[zteam]], maxflow))
        else:
            lowflow_teams.append((zteam, scores[teams[zteam]]))

challenging_teams = sorted(challenging_teams, key=lambda x: (x[1], x[0]), reverse=True)
elimnated_teams = sorted(elimated_teams, key=lambda x: (x[1], x[0]), reverse=True)
lowflow_teams = sorted(lowflow_teams, key=lambda x: (x[1], x[0]), reverse=True)

print("Teams still challenging are...")
for i in range(len(challenging_teams)):
    print(challenging_teams[i][0].rstrip('\n') + " " + str(challenging_teams[i][1]) + " (flow = " + str(challenging_teams[i][2]) + ")")

print("\nTeams that have been eliminated are...")
for i in range(len(lowflow_teams)):
    print(lowflow_teams[i][0].rstrip('\n') + " " + str(lowflow_teams[i][1]) + " (due to smaller max flow)")
for i in range(len(elimnated_teams)):
    print(elimnated_teams[i][0].rstrip('\n') + " " + str(elimnated_teams[i][1]) + " (as it cannot catch up)")
