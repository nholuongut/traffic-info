from random import randint

class Street():
    def __init__(self, name, beginning, ending, length):
        self.name = name
        self.beginning = beginning
        self.ending = ending
        self.length = length
    
    def getDict(self):
        return {
                    'name': self.name,
                    'beginning': self.beginning,
                    'ending': self.ending,
                    'length': self.length
                }

class Trecho():
    def __init__(self, street, beginning, direction):
        self.street = street
        self.beginning = beginning
        self.num_cars = 0
        self.num_acc = 0
        self.direction = direction

    def getDict(self):
        return {
                    'street': self.street,
                    'beginning': self.beginning,
                    'num_cars': self.num_cars,
                    'num_acc': self.num_acc,
                    'direction': self.direction
                }
    def car_entered(self):
        self.num_cars += 1

    def car_left(self):
        self.num_cars -= 1

    def accident(self):
        self.num_acc += 1

    def accident_take_care(self):
        self.num_acc -= 1

squareX = 5
squareY = 5

stNames = open("streetName.csv", 'r')
streets = []

for i in range(squareX+1):
    vertical_street_beginning = (i, 0)
    vertical_street_ending = (i, 5)
    horizontal_street_beginning = (0,i)
    horizontal_street_ending = (5,i)
    vertical_stName = stNames.readline().split(",")[0]
    horizontal_stName = stNames.readline().split(",")[0]
    streets.append(Street(vertical_stName, vertical_street_beginning, vertical_street_ending, 5).getDict())
    streets.append(Street(horizontal_stName, horizontal_street_beginning, horizontal_street_ending, 5).getDict())

print("Streets") 
print(streets)

trechos = []

for street in streets:
    street_name = street['name']
    beg_street = street['beginning']
    end_street = street['ending']
    for i in range(5):
        ## Check if it's vertical or horizontal
        if beg_street[0]==end_street[0]:
            beg_trecho_lr = (beg_street[0], i)
            beg_trecho_rl = (beg_street[0], 5-i)
            trechos.append(Trecho(street_name, beg_trecho_lr, True).getDict())
            trechos.append(Trecho(street_name, beg_trecho_rl, False).getDict())
        else:
            beg_trecho_ud = (i, beg_street[1])
            beg_trecho_du = (5-i, beg_street[1])
            trechos.append(Trecho(street_name, beg_trecho_ud, True).getDict())
            trechos.append(Trecho(street_name, beg_trecho_du, False).getDict())

print("Trechos")
print(trechos)
'''
for i in range(1):
    stName = stNames.readline().split(',')[0]
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
    #st = Street(stName, (0,1), squareX, 20)'''

