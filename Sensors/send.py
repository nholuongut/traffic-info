#!/usr/bin/env python
import pika
import json
import time
from random import randint, choice, gauss
import os
import sys
import string
import requests
import math


#MAKE CONNECTION
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
#SET QUEUE
channel.queue_declare(queue='cars')
channel.queue_declare(queue='otherSensors')


class Sensor:
    def __init__(self, neighboursFile):

        #INITIALIZE DATA
        f = open(neighboursFile, "r")
        self.neighbours = json.loads(f.read())
        f.close()
        self.number_of_trechos = len(self.neighbours)

        self.cityname = neighboursFile[:-4]

        self.first = int(list(self.neighbours.keys())[0])
        self.last = int(list(self.neighbours.keys())[-1])

        self.actual_info = {}
        
        req=json.loads(requests.get('http://192.168.160.237:8000/licenses_by_city/' + self.cityname + '/').content)
        print(req)
        for trecho in req:
            self.actual_info[trecho["id"]] = trecho["licenses"]
        #for i in range(self.first,self.last+1):
        #    self.actual_info[i] = []

    def add(self,trecho, plate):
        msg = json.dumps({"type": "insert", "id" : trecho, "plate":plate, "city":self.cityname})
        #print(msg)
        channel.basic_publish(exchange='', routing_key='cars', body=msg)

    def remove(self,trecho, plate):
        msg = json.dumps({"type": "delete", "id" : trecho, "plate":plate , "city":self.cityname})
        #print(msg)
        channel.basic_publish(exchange='', routing_key='cars', body=msg)

    def printInfo(self):
        #os.system('clear')
        n = 0
        for trecho in self.actual_info:
            if 'TESTE1' in self.actual_info[trecho]:
                n = trecho

            if len(self.actual_info[trecho]) > 80:
                print("Trecho %-2d : %-4d" % (trecho, len(self.actual_info[trecho])))

        print('--------------------------------')

        for trecho in self.actual_info:
            if len(self.actual_info[trecho]) < 20:
                print("Trecho %-2d : %-4d" % (trecho, len(self.actual_info[trecho])))

        print('TESTE1 in ' + str(n))


    def forceTraffic(self):
        trecho = randint(self.first, self.last)
        while len(self.actual_info[trecho]) < 80:
            plate = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(6))
            self.actual_info[trecho].append(plate)
            self.add(trecho, plate)
            time.sleep(0.05)


    def reduceTraffic(self):
        highTraffic = {}
        for trecho in self.actual_info:
            if len(self.actual_info[trecho]) >= 80:
                highTraffic[trecho] = len(self.actual_info[trecho])

        mostCars = [i[0] for i in sorted(highTraffic.items(), key= lambda e : (e[1], e[0]), reverse=True)]

        for i in range(len(mostCars)):
            if i == 5 :
                break
            
            trecho = mostCars[i]

            while len(self.actual_info[trecho]) > 50:
                trechoOut = self.neighbours[str(trecho)][randint(0, len(self.neighbours[str(trecho)])-1)]
                plateOut = self.actual_info[trecho][randint(0, len(self.actual_info[trecho])-1)]

                disapear = randint(0,1) == 0
                if disapear:
                    if plateOut != 'TESTE1':
                        self.actual_info[trecho].remove(plateOut)
                        self.remove(trecho, plateOut)
                else:
                    self.actual_info[trecho].remove(plateOut)
                    self.remove(trecho, plateOut)

                    self.actual_info[trechoOut].append(plateOut)
                    self.add(trechoOut, plateOut)
                time.sleep(0.05)

    def populate(self):
        print("populating")
        self.add(self.first, 'TESTE1')
        self.actual_info[self.first].append('TESTE1')

        for i in range(randint(self.number_of_trechos*20, self.number_of_trechos * 70)):
            trecho = randint(self.first, self.last)
            plate = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(6))

            self.actual_info[trecho].append(plate)
            self.add(trecho, plate)
    
    def visibility(self, req):
        #req=json.loads(requests.get('http://192.168.160.237:8000/info_street').content)
        temp_data={d['id']:d['visibility'] for d in req }

        random_alter=[choice(list(temp_data.keys())) for i in range(math.floor(len(temp_data)/5))]
        for d in random_alter:
            temp_data[d]=min(100,max(0,math.ceil(gauss(60,25))))
            
        #[print(f"ID- {d} Value-{temp_data[d]}") for d in temp_data]
        [channel.basic_publish(exchange='', routing_key='otherSensors', body=json.dumps({"type":"visibility", "id":d, "visibility": temp_data[d], "city":self.cityname} )) for d in temp_data]

    
    def roadBlock(self,req):    
        
        data={d['id']:True if d['transit_type']=='Blocked' else False for d in req }
        # Generating positive values to go negative and negative to go positive
        data_positive=[d for d in data if data[d]==True] # Blocked
        data_negative=[d for d in data if data[d]==False] # Not Blocked
        random_data_positive=[]
        random_data_negative=[]
        if len(data_positive)!=0:
            for i in range(min(5,len(data_positive))):
                choicee=choice(data_positive)
                if choicee not in random_data_positive:
                    random_data_positive.append(choicee)

        if len(data_negative)!=0:
            for i in range(min(2,len(data_negative))):
                choicee=choice(data_negative)
                if choicee not in random_data_negative:
                    random_data_negative.append(choicee)


        json_update_true=[{"type":"roadblock_down","id":d, "city":self.cityname} for d in random_data_positive] # Blocked
        json_update_false=[{"type":"roadblock_up","id":d, "city":self.cityname} for d in random_data_negative] # Not blocked

        for i in json_update_true:
            #r=requests.delete("http://192.168.160.237:8000/roadblock/",data=json.dumps(i),headers={"Content-Type":"text/plain"})
            channel.basic_publish(exchange='', routing_key='otherSensors', body=json.dumps(i))

        for f in json_update_false:
            #r=requests.put("http://192.168.160.237:8000/roadblock/",data=json.dumps(f),headers= {"Content-Type":"text/plain"})
            channel.basic_publish(exchange='', routing_key='otherSensors', body=json.dumps(f))

    def police(self, req):
        data={d['id']:d['police'] for d in req}

        # Generating positive values to go negative and negative to go positive
        data_positive=[d for d in data if data[d]==True]
        data_negative=[d for d in data if data[d]==False]
        if len(data_positive)!=0:
            random_data_positive=[choice(data_positive) for i in range(min(5,len(data_positive)))]
            json_update_true=[json.dumps({"type":"police_down","id":d, "city":self.cityname}) for d in random_data_positive]
            [channel.basic_publish(exchange='', routing_key='otherSensors', body=i) for i in json_update_true]

        if len(data_negative)!=0:
            random_data_negative=[choice(data_negative) for i in range(min(2,len(data_negative)))]
            json_update_false=[json.dumps({"type":"police_up","id":d, "city":self.cityname}) for d in random_data_negative]
            [channel.basic_publish(exchange='', routing_key='otherSensors', body=i) for i in json_update_false]
    
    def accident(self,req):
        data={d['id']:{"accident":d['n_accident'],"x_coord":[d["beginning_coords_x"],d["ending_coords_x"]],"y_coord":[d["beginning_coords_y"],d["ending_coords_y"]]} for d in req }
        # Generating positive values to go negative and negative to go positive
        data_positive=[d for d in data if data[d]["accident"]>0] # Has accident
        data_negative=[d for d in data if data[d]["accident"]==0] # No accident

        #print(f"ACCIDENT {len(data_positive)}")
        #print(f"NO ACCIDENT {len(data_negative)}")       

        random_data_positive=[]
        random_data_negative=[]

        if len(data_positive)!=0:
            for i in range(min(10,len(data_positive))):
                choicee=choice(data_positive)
                if choicee not in random_data_positive:
                    random_data_positive.append(choicee)

        if len(data_negative)!=0:
            for i in range(min(4,len(data_negative))):
                choicee=choice(data_negative)
                if choicee not in random_data_negative:
                    for i in range(randint(0,2)):
                        random_data_negative.append(choicee)

        json_update_true=[{"id":d} for d in random_data_positive] # Blocked

        json_update_false=[{"id":d,
        "x_coord":randint(min(data[d]["x_coord"][0],data[d]["x_coord"][1]),max(data[d]["x_coord"][0],data[d]["x_coord"][1])),
        "y_coord":randint(min(data[d]["y_coord"][0],data[d]["y_coord"][1]),max(data[d]["y_coord"][0],data[d]["y_coord"][1]))}
        for d in random_data_negative] # Not blocked, going to be

        #print(json_update_true)
        #print(json_update_false)
        for i in json_update_true:
            i["type"] = "accident_down"
            channel.basic_publish(exchange='', routing_key='otherSensors', body=json.dumps(i))

        for f in json_update_false:
            f["type"] = "accident_up"
            channel.basic_publish(exchange='', routing_key='otherSensors', body=json.dumps(f))


    def startSensor(self):

        #SENSOR
        i = 1 
        #self.printInfo()
        
        while True:
            if i % 50 == 0:
                #self.printInfo()
                pass

            if i % 500 == 0:
                req=json.loads(requests.get('http://192.168.160.237:8000/info_street/' + self.cityname + '/').content)
                self.visibility(req)
                self.roadBlock(req)   
                self.police(req)
                self.accident(req)
                self.forceTraffic() 

            if i % 2000 == 0:
                self.reduceTraffic()

            trecho = randint(self.first,self.last)
            trechoOut = self.neighbours[str(trecho)][randint(0, len(self.neighbours[str(trecho)])-1)]

            if len(self.actual_info[trecho]) != 0:
                plateOut = self.actual_info[trecho][randint(0, len(self.actual_info[trecho])-1)]
                self.actual_info[trecho].remove(plateOut)
                self.actual_info[trechoOut].append(plateOut)

                self.remove(trecho, plateOut)
                self.add(trechoOut, plateOut)
            
            i+=1
            if i == 10000:
                i = 1
            time.sleep(0.05)


sensor = Sensor(sys.argv[1])
try:
    if sys.argv[2] == "populate":
        sensor.populate()
except:
    sensor.startSensor()

connection.close()
