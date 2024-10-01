import json
import sys

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    if (A == D):        #special case
        return False
    if (B == C):
        return True     #special case
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


neighbours = {}

f = open(sys.argv[1], "r")
trechos = json.loads(f.read())
f.close()

#trechos = trechos['Trechos']

for trecho in trechos:
    begT1 = [trecho["beginning_coords_x"], trecho["beginning_coords_y"]]
    endT1 = [trecho["ending_coords_x"],trecho["ending_coords_y"]]
    neighbours[trecho["id"]] = []

    for trecho2 in trechos:

        begT2 = [trecho2["beginning_coords_x"], trecho2["beginning_coords_y"]]
        endT2 = [trecho2["ending_coords_x"],trecho2["ending_coords_y"]]

            
        if (trecho["id"] == trecho2["id"]) or (begT1 == endT2 and begT2 == endT1):    #same street
            continue

        if intersect(begT1, endT1, begT2, endT2):
            neighbours[trecho["id"]] += [trecho2["id"]]
    

f = open("neighbours.txt", "w")
f.write(json.dumps(neighbours, indent=4))
f.close()
