#!/usr/bin/env python
import pika
import json
import requests
import time
from threading import Thread

t = time.time()
queues = {'Ilhavo':[], 'Roma':[], 'Porto':[]}


def callback(ch, method, properties, body):
    global queues
    global t
    body = json.loads(body)
    #print(body)
    if body["type"] in ["insert", "delete"]:
        if body['city'] == 'Ilhavo':
            body.pop('city', None)
            queues['Ilhavo'].append(body)
        elif body['city'] == 'Roma':
            body.pop('city', None)
            queues['Roma'].append(body)
        elif body['city'] == 'Porto':
            body.pop('city', None)
            queues['Porto'].append(body)

    for city in queues:
        if len(queues[city]) == 100:
            msg = json.dumps({"type":"various_cars", "city": city, "data":queues[city]})
            print(msg)
            a=requests.post("http://192.168.160.237:8000/car/", data = msg, headers={"Content-Type":"text/plain"})
            print(a)
            while str(a)=="<Response [500]>":
                a=requests.post("http://192.168.160.237:8000/car/", data = msg, headers={"Content-Type":"text/plain"})
                print(a)
            queues[city] = []
            t = time.time()


def othercallback(ch, method, properties, body):
    body = json.loads(body)
    if body["type"] == "visibility":
        msg = json.dumps({"id" : body["id"], "visibility": body["visibility"]})
        print(msg)
        r=requests.put("http://192.168.160.237:8000/visibility/", data = msg, headers={"Content-Type":"text/plain"})
        print(r)
    elif body["type"] == "roadblock_down":
        msg = json.dumps({"id" : body["id"]})
        print(msg)
        print("rdown")
        r=requests.delete("http://192.168.160.237:8000/roadblock/", data = msg, headers={"Content-Type":"text/plain"})
        print(r)
    elif body["type"] == "roadblock_up":
        msg = json.dumps({"id" : body["id"]})
        print(msg)
        print("rup")
        r = requests.post("http://192.168.160.237:8000/roadblock/", data = msg, headers={"Content-Type":"text/plain"})
        print(r)
    elif body["type"] == "police_down":
        msg = json.dumps({"id" : body["id"]})
        print(msg)
        r=requests.delete("http://192.168.160.237:8000/police/", data = msg, headers={"Content-Type":"text/plain"})
        print(r)
    elif body["type"] == "police_up":
        msg = json.dumps({"id" : body["id"]})
        print(msg)
        r=requests.put("http://192.168.160.237:8000/police/", data = msg, headers={"Content-Type":"text/plain"})
        print(r)
    elif body["type"] == "accident_down":
        msg = json.dumps(body)
        print(msg)
        r=requests.delete("http://192.168.160.237:8000/accident/",data=msg,headers={"Content-Type":"text/plain"})
        print(r)
    elif body["type"] == "accident_up":
        msg = json.dumps(body)
        print(msg)
        r=requests.post("http://192.168.160.237:8000/accident/",data=msg,headers={"Content-Type":"text/plain"})
        print(r)


def consumeOtherSensors():
    channel.basic_consume(
        queue='otherSensors', on_message_callback=othercallback, auto_ack=True)



#MAKE CONNECTION
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#SET QUEUE
channel.queue_delete(queue='cars')
channel.queue_delete(queue='otherSensors')

channel.queue_declare(queue='cars')
channel.queue_declare(queue='otherSensors')

thread = Thread(target = consumeOtherSensors)
thread.start()
thread.join()

channel.basic_consume(
    queue='cars', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

#START CONSUMING
channel.start_consuming()
