from random import randint
import json
import unicodedata
import math

import sys

class Street():
    def __init__(self, name, beginning, ending):
        self.name = unicodedata.normalize('NFD',name).encode('ascii','ignore').decode('utf-8')  #remove accents
        self.beginning = beginning
        self.ending = ending
    
    
    def getDict(self):
        return {
                    "name": self.name,
                    "beginning_coords": self.beginning,
                    "ending_coords": self.ending,
                }

class Trecho():
    def __init__(self, id, street, beginning, ending, direction):
        self.street = unicodedata.normalize('NFD',street).encode('ascii','ignore').decode('utf-8')  #remove accents
        self.beginning = beginning
        self.ending = ending
        self.num_cars = 0
        self.num_acc = 0
        self.direction = direction
        self.id = id
    def getDict(self):
        return {
                    "id": self.id,
                    "street": self.street,
                    "beginning_coords_x": self.beginning[0],
                    "beginning_coords_y": self.beginning[1],
                    "ending_coords_x": self.ending[0],
                    "ending_coords_y": self.ending[1],
                    "number_cars": self.num_cars,
                    "accident": self.num_acc,
                    "actual_direction": self.direction
                }

def calclen(p1,p2):
    return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )


squareX = 2000
squareY = 2000

step = 500
stNames = open("streetName.csv", "r")
streets = []

#GENERATE STREETS
for i in range(0,squareX+1, 500):
    vertical_street_beginning = (i, 0)
    vertical_street_ending = (i, squareY)
    vertical_stName = stNames.readline().split(",")[0]
    streets.append(Street(vertical_stName, vertical_street_beginning, vertical_street_ending).getDict())

for i in range(0, squareY+1, 500):
    horizontal_street_beginning = (0, i)
    horizontal_street_ending = (squareX, i)
    horizontal_stName = stNames.readline().split(",")[0]
    streets.append(Street(horizontal_stName, horizontal_street_beginning, horizontal_street_ending).getDict())

print(len(streets))


#GENERATE TRECHOS

data = {"Streets" : streets}
trechos = []
id = 0
for street in streets:
    street_name = street["name"]
    beg_street = street["beginning_coords"]
    end_street = street["ending_coords"]
    length = int(calclen(beg_street,end_street))
    for i in range(0, length, step):


        ## Check if it"s vertical or horizontal
        if beg_street[0]==end_street[0]:        #V
            beg_trecho_du = (beg_street[0], i)
            end_trecho_du = (beg_street[0], i+step)
            beg_trecho_ud = (beg_street[0], squareY-i)
            end_trecho_ud = (beg_street[0], squareY-i - step)

            trechos.append(Trecho(id, street_name, beg_trecho_du, end_trecho_du, True).getDict())
            trechos.append(Trecho(id + 1, street_name, beg_trecho_ud, end_trecho_ud, False).getDict())
        else:   #H
            beg_trecho_lr = (i, beg_street[1])
            end_trecho_lr = (i + step , beg_street[1])
            beg_trecho_rl = (squareX-i, beg_street[1])
            end_trecho_rl = (squareX-i - step, beg_street[1])

            trechos.append(Trecho(id, street_name, beg_trecho_lr, end_trecho_lr, True).getDict())
            trechos.append(Trecho(id +1, street_name, beg_trecho_rl, end_trecho_rl, False).getDict())

        id += 2
data['Trechos'] = trechos


print(json.dumps(streets, indent=4))
f = open("very_primordial_data.txt", "w")
f.write(json.dumps(streets, indent=4))
f.close()








"""
for i in range(1):
    stName = stNames.readline().split(",")[0]
    ## Random for vertical vs horizontal streets
    is_horizontal = randint(0,1) == 1
    common_var = 0
    diff_var1 = 0
    diff_var2 = 0
    if is_horizontal:
        common_var = randint(0, squareY)
        diff_var1 = randint(0, squareY)
        diff_var2 = randint(0, squareY)
        begin, end = sorted([x1, x2])
        print(f"Street {stName}, starts at {(begin, common_y)} ends at {(end, common_y)}")
    else:
        common_x = randint(0, squareY)
        y1 = randint(0, squareX)
        y2 = randint(0, squareX)
        begin, end = sorted([y1, y2])
        print(f"Street {stName}, starts at {(begin, y1)} ends at {(end, y2)}")
    #st = Street(stName, (0,1), squareX, 20)"""

