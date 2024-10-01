#change the ending/beg coords

import json
import sys

# f = open("stuff.txt", "w")
# f.write(json.dumps(stuff, indent=4))
# f.close()

f = open(sys.argv[1], "r")
stuff = json.loads(f.read())
f.close()

for i in range(len(stuff)-1):
    if (stuff[i]["beginning_coords_x"] == stuff[i+1]["beginning_coords_x"]
        and stuff[i]["beginning_coords_y"] == stuff[i+1]["beginning_coords_y"]
        and stuff[i]["ending_coords_x"] == stuff[i+1]["ending_coords_x"]
        and stuff[i]["ending_coords_y"] == stuff[i+1]["ending_coords_y"]):

        assert(not stuff[i+1]["actual_direction"])

        tmpx = stuff[i+1]["ending_coords_x"]
        tmpy = stuff[i+1]["ending_coords_y"]

        stuff[i+1]["ending_coords_x"] = stuff[i+1]["beginning_coords_x"]
        stuff[i+1]["ending_coords_y"] = stuff[i+1]["beginning_coords_y"] 
        stuff[i+1]["beginning_coords_x"] = tmpx 
        stuff[i+1]["beginning_coords_y"] = tmpy 
        
        print(i)
        i+=1

f = open("stuff.txt", "w")
f.write(json.dumps(stuff, indent=4))
f.close()

