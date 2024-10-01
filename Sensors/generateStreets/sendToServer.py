import json
import requests

f = open("mapa3.txt", "r")
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

f = open(cityname + "City.txt", "w")
f.write(json.dumps(req, indent=4))
f.close()

