import requests
import time
import json
for i in range(3):
    r=requests.put("http://127.0.0.1:8000/car/",data=json.dumps({
	"id":10}))
    print(r.text)
    time.sleep(0.01)