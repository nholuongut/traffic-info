# Data Generation  

- City creation  
- Sensor Virtualization  

## City creation  

In order to watch this project working we needed to intruduce citys to the DataBase.  
A set of streets belonging to a city was generated with Python script and fed to the API. After the insertion of the data, a set of Sections was returned that will be used later on.  

## Sensor Virtualization  

The objective with this part of data generation is to sucessefully substitute real sensors by a script that generates data in a aproxymate way.  
We could opt to create a set of static messages to recreate the same scenario every time but we decided to go for a more bold move and let the messages be created randomly by a somewhat consistent virtual sensor.  
Initially, our intention was have a raspberry generating full time data for us, but since we could not get one in time and probably wasn worth it (due to the low computacional campacity), we decided to run this sensors in or own PCs.  

The previously returned sections are divisions of the sent streets and are needed for the next step (virtualization of sensor data). It was needed to run a few more python scripts on this sections to put them in the desired way, for example find all the connections between Sections so that in the simulation, cars would go from one section to another without magicaly appearing in the order side of the map. Note as well that this responsability should not be from the server, as this consistency in sensor virtualization would not be a concern in a real word project.  

>python3 doEverything.py fileContainingStreets CityName  

Would send the server the information required to create a city as well as processing the returning data in the desired way. The result, a file named CityName.txt wich would be fed to the sensors script (this file contains the connections of every section to facilitate consistency).  

### Send.py

Send.py is the main script of data generation. It's job is to produce sensor like messages and store them in rabbit-MQueu queues.  
In total, sensors registes 5 types of messages:  

- Car moviments,
- Police Location,
- Road blocked,
- Accident Location,
- Visibility.  

As said before, this messages are stored in 2 Rabbit-MQueu queues (Car moviments gets a queu for his own due to intensive frequency and to prevent unsynchronization issues in the other messages).  
Without getting in unecessary details, this script uses one of the API get methods to have an idea of the internal state of the data in the DataBase, and then, from there continuosly generates messages to get the simulation running.  
Note, that the information about cars and sections is only asked once, and from there the script keeps a representation of the data so that the server doesn't need to perform unecessary work.  
All the other messages are not very costly so before creating them the server gives information about police locations, etc.

The messages are json Objects, for example:

- {"type": "insert", "id" : 5, "plate":AL16PO, "city": "Ilhavo"}
- {"type":"visibility", "id":6, "visibility": 50, "city":"Ilhavo"}

>python3 send.py ConnectionsFile(retured by doEverything.py)  

### Receive.py

Receive.py is the consumer of rabbit-MQueue and his objective is to process and forward the sensor messages to the server using the API methods.  
Since the there are a lot of car moviments messages and our group had issues with performance in early tests, this data is sent in *bulk mode* to the server to minimize the communication between this end of the queue and the server (100 messages are aggregated before they are sent to the server).

>python3 receive.py  

We can have has many sends running (1 for each city) as we want, but we only need one receive.