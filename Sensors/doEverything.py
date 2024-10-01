import json
import requests
import sys
#-------------------------SEND MAP TO DB
f = open(sys.argv[1], "r")
streets = json.loads(f.read())
f.close()

trechos = []
cityname = sys.argv[2]
  
for street in streets:
    street["city"] = cityname
    #print(street)

    r=requests.post('http://192.168.160.237:8000/street/', data=json.dumps(street), headers={"Content-Type":"text/plain"})
    print(r)

req = requests.get('http://192.168.160.237:8000/info_street/' + cityname + '/').content
req=json.loads(req)


#----------------------------TRANSFORM

for i in range(len(req)-1):
    if (req[i]["beginning_coords_x"] == req[i+1]["beginning_coords_x"]
        and req[i]["beginning_coords_y"] == req[i+1]["beginning_coords_y"]
        and req[i]["ending_coords_x"] == req[i+1]["ending_coords_x"]
        and req[i]["ending_coords_y"] == req[i+1]["ending_coords_y"]):

        assert(not req[i+1]["actual_direction"])

        tmpx = req[i+1]["ending_coords_x"]
        tmpy = req[i+1]["ending_coords_y"]

        req[i+1]["ending_coords_x"] = req[i+1]["beginning_coords_x"]
        req[i+1]["ending_coords_y"] = req[i+1]["beginning_coords_y"] 
        req[i+1]["beginning_coords_x"] = tmpx 
        req[i+1]["beginning_coords_y"] = tmpy 
        
        print(i)
        i+=1

#------------------------GENERATE NEIGHBOURS
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


#trechos = trechos['Trechos']

for trecho in req:
    begT1 = [trecho["beginning_coords_x"], trecho["beginning_coords_y"]]
    endT1 = [trecho["ending_coords_x"],trecho["ending_coords_y"]]
    neighbours[trecho["id"]] = []

    for trecho2 in req:

        begT2 = [trecho2["beginning_coords_x"], trecho2["beginning_coords_y"]]
        endT2 = [trecho2["ending_coords_x"],trecho2["ending_coords_y"]]

            
        if (trecho["id"] == trecho2["id"]) or (begT1 == endT2 and begT2 == endT1):    #same street
            continue

        if intersect(begT1, endT1, begT2, endT2):
            neighbours[trecho["id"]] += [trecho2["id"]]
    

f = open(sys.argv[2] + ".txt", "w")
f.write(json.dumps(neighbours, indent=4))
f.close()

