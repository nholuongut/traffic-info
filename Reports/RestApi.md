# REST API Documentation

# GETS
## Get all streets of a certain city
```mermaid
graph LR;
A((GET));B['/info_street/< string:city >/']
A -- REQUEST --> B
```
### Possible HTTP Responses
> **HTTP_200_OK** -> Returns an array of dictionaries containing information about the current state of each section for that specific city 

> **HTTP_400_BAD_REQUEST**

**Example**
**GET ``` /info_street/Aveiro/```**
```python
[{
        "id": 1,
        "number_cars": 0,
        "actual_direction": true,
        "n_accident": 0,
        "beginning_coords_x": 0,
        "beginning_coords_y": 0,
        "ending_coords_x": 0,
        "ending_coords_y": 500,
        "street": {
            "name": "Rua Tenente Joaquim Lopes Craveiro",
            "id": 1
        },
        "transit_type": "Normal",
        "police": false,
        "visibility": 100
    }

    ... 
    ...
}] 
```

## Get all cars of a certain section of a street
```mermaid
graph LR;
A((GET));B[ '/all_cars/<int:section_id >/' ]
A -- REQUEST --> B
```
### Possible HTTP Responses**
 > **HTTP_200_OK** -> Returns an array of dictionaries containing the license plate and the section

 > **HTTP_400_BAD_REQUEST**
 
 > **HTTP_404_NOT_FOUND**


**Example**
**GET  ``` /all_cars/1```**
```python
[
    {
        "license_plate": "mota10",
        "section": 1
    },
    {
        "license_plate": "mota11",
        "section": 1
    }
]
```

## Get statistics of a certain street with a beginning and end time
```mermaid
graph LR; 
A((GET));B[ statistics/< int:street_id >/< str:begin >/< str:end >/ ]
A -- REQUEST --> B
```
### Possible HTTP Responses
 > **HTTP_200_OK** -> Returns a dictionare with the name of the street, number of times that it got transit (in minutes), with roadblocks and total accidents during that time frame

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

**Example**
**GET  ``` /statistics/1/2017-12-31/2019-12-31/```**
```python
{
    "name": "Rua Tenente Joaquim Lopes Craveiro",
    "transit_count": 15,
    "road_block": {
        "total_time": 500,
        "times": 1
    },
    "total_accident": 4
}
```

## Get statistics of a certain street with a beginning and end time that happen on a specific week day (Monday,Friday,...)
```mermaid
graph LR; 
A((GET));B[ statistics/< int:street >/< str:begin >/< str:end >/< str:week_day >/ ]
A -- REQUEST --> B
```
**Possible HTTP Responses**

 > **HTTP_200_OK**-> Returns a dictionary with the name of the street, number of times that it got transit (in minutes), with roadblocks and total accidents during that time frame but that only in that specific week day 

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**


**Example**
**GET  ``` /statistics/1/2017-12-31/2019-12-31/Monday/```**
```python
{
    "name": "Rua Tenente Joaquim Lopes Craveiro",
    "transit_count": 10,
    "road_block": {
        "total_time": 500,
        "times": 1
    },
    "total_accident": 3
}
```

## Get all the streets of a give city

```mermaid
graph LR; 
A((GET));B[ 'all_streets_city/<str:city_name>>' ]
A -- REQUEST --> B
```
**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns a list of dictionaries containing the id and name of the streets of the city , being that key represents the id and value represents the name

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**


**Example**
**GET  ``` /all_streets_city/Ilhavo/```**
```python
[
    {
        "key": 1,
        "value": "Rua Tenente Joaquim Lopes Craveiro"
    },
    {
        "key": 2,
        "value": "Rua de Caveiros"
    }

    ...
    ...
]
```
## Get all the licenses plates (Cars) in every section of a specific city

```mermaid
graph LR; 
A((GET));B[ 'licenses_by_city/<str:city>/' ]
A -- REQUEST --> B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns an array with a dictionary having the key as the section id and licenses being a list with all the license_plates in that section. All the sections belong to the city passed in the URL

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**


**Example**
**GET  ``` /licenses_by_city/Aveiro/```**
```python
[
    {
        "id": 1,
        "licenses": [
            "mota10",
            "mota11"
        ]
    },
    {
        "id": 2,
        "licenses": [
            "mota12"
        ]
    }
    
    ...
    ...
]

```
## Track a specific car

```mermaid
graph LR; 
A((GET));B[ 'specific_car/<str:license_plate>/' ]
A -- REQUEST --> B
```
___
# WARNING License Plate is case sensitive
___
**Possible HTTP Responses**

 > **HTTP_200_OK**-> Returns a dictionary with the wanted license plate and the section it is in

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**


**Example**
**GET  ``` /specific_car/mota10/```**
```python
{
    "license_plate": "mota10",
    "section": 1
}
```
## Get the number of a specific type of incident (accidents...) in a street for each day in a time frame 

```mermaid
graph LR; 
A((GET));B[ 'charts/ <str:type>/street=<int:street_id>&start_date=<str:begin>&end_date=<str:end>/' ]
A -- REQUEST --> B
```
___
# WARNING Dates should be passed with Year-Month-Day, otherwise a BAD_REQUEST will be thrown
___
**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns a dictionary contains two lists, one with the days and another with the ammount of incident that occured in that day. The index of list 1 corresponds to the same index of list two. In the following example this means that in 2019-12-16 the street with id 1 had 3 incidents of type accident

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**


**Example**
**GET   ``` /charts/accident/street=1&start_date=2019-12-12&end_date=2019-12-22/```**
```python
{
   {
    "Days": [
        "2019-12-12",
        "2019-12-13",
        "2019-12-14",
        "2019-12-15",
        "2019-12-16",
        "2019-12-17",
        "2019-12-18",
        "2019-12-19",
        "2019-12-20",
        "2019-12-21"
    ],
    "ammount": [
        0,
        0,
        0,
        0,
        3,
        0,
        0,
        0,
        0,
        0
    ]
}
}
```

## Get all available cities in the database

```mermaid
graph LR; 
A((GET));B[ 'available_cities/' ]
A -- REQUEST --> B
```
___
# WARNING Cities is case sensitive
___
**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns a list with all the cities currently mapped in the database

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**


**Example**
**GET   ``` /available_cities/```**
```python
[
    "Aveiro",
    "Porto"
]
```

# PUTS
## Alter the visibility of a given section
```mermaid
graph LR; 
A((PUT));
B[ 'visibility/' ];
C["{'id':<int:section_id>,'visibility':<int:visibility_value>}"];
A -- REQUEST --> C -->B
```
___
# WARNING Visibility is a number between 0 and 100
___
**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns the section in which the visibility changed and all the other attributes of that section

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

**Example**
**PUT   ``` /visibility/```**
```python
INPUT:
{
	"id":1,
	"visibility":50
}
OUTPUT:
{
    "id": 1,
    "number_cars": 0,
    "actual_direction": true,
    "n_accident": 0,
    "beginning_coords_x": 0,
    "beginning_coords_y": 0,
    "ending_coords_x": 0,
    "ending_coords_y": 400,
    "street": {
        "name": "Rua Tenente Joaquim Lopes Craveiro",
        "id": 1
    },
    "transit_type": "Normal",
    "police": false,
    "visibility": 50
}
```

## Add police to a given section
```mermaid
graph LR; 
A((PUT));
B[ 'police/' ];
C["{'id':<int:section_id>}"];
A -- REQUEST --> C -->B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns the section in which the police changed to True and all the other attributes of that section

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

**Example**
**PUT   ``` /police/```**
```python
INPUT:
{
	"id":1,
}
OUTPUT:
{
    "id": 1,
    "number_cars": 0,
    "actual_direction": true,
    "n_accident": 0,
    "beginning_coords_x": 0,
    "beginning_coords_y": 0,
    "ending_coords_x": 0,
    "ending_coords_y": 400,
    "street": {
        "name": "Rua Tenente Joaquim Lopes Craveiro",
        "id": 1
    },
    "transit_type": "Normal",
    "police": true,
    "visibility": 50
}
```

# POSTS

## Create a new street
```mermaid
graph LR; 
A((POST));
B[ 'street/' ];
C["{'name':<str:street_name>,'beginning_coords':[<int:x_coord>,<int:y_coord>,'ending_coords':[<int:x_coord>,<int:y_coord>],'city':<str:city_name>}"];
A -- REQUEST --> C -->B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns the street with all its values. Having some that are defined by the sever

 > **HTTP_400_BAD_REQUEST**

**Example**
**POST  ``` /street/```**
```python
INPUT:
{
    "name": "Rua Tenente Joaquim Lopes Craveiro",
    "beginning_coords": [
        0,
        0
    ],
    "ending_coords": [
        0,
        2000
    ],
    "city":"Ilhavo"
}
OUTPUT:
{
    "name": "Rua Tenente Joaquim Lopes Craveiro",
    "begin_coord_x": 0,
    "begin_coord_y": 0,
    "ending_coord_x": 0,
    "ending_coord_y": 2000,
    "length": 2000,
    "city": "Ilhavo"
}
```

## Add and remove cars to a certain section
## The rabbitmq should execute an aggregation function

```mermaid
graph LR; 
A((POST));
B[ 'car/' ];
C["{'type':'various_cars','city':<str:city_name>},'data':[{'type':('delete' | 'insert'),'id':<int:section_id>,'plate':<str>}, ...]"];
A -- REQUEST --> C -->B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> HTTP_200_OK means every CRUD OPERATION in the aggregation was executed

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

**Example**
**POST   ```/car/```**
```python
INPUT:
{
    "type":"various_cars",
    "city":"Ilhavo",
    "data":[
        {"type":"delete","id":1,"plate":"mota10"},
        {"type":"insert","id":1,"plate":"tomas1"},
    ]
}
OUTPUT:
<HTTP_200_OK>
```

## Update the accident information of a section

```mermaid
graph LR; 
A((POST));
B[ 'accident/' ];
C["{'id':<int:section_id>,'x_coord':<int>,'y_coord':<int>}"]
A -- REQUEST --> C --> B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns the coords of the accident, the section and the time in which the server registered the accident

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

**Example**
**POST   ``` /accident/```**
```python
INPUT:
{
    "id":1,
    "x_coord":20,
    "y_coord":20
}
OUTPUT:
{
    "coord_x": 20,
    "coord_y": 20,
    "date": "2019-12-18T00:06:54.533982Z",
    "section": 1
}
```

## Update roadblock information of a section
```mermaid
graph LR; 
A((POST));
B[ 'roadblock/' ];
C["{'id':<int:section_id>"];
A -- REQUEST --> C -->B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns the following string 'Road blocked'

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

 > **HTTP_304_NOT_MODIFIED** -> Returns the following string 'A road can only be blocked once'

**Example**
**POST   ``` /roadblock/```**
```python
INPUT:
{
    "id":1,
}
OUTPUT:
'Road Blocked'
```

# DELETE

## Remove police to a given section
```mermaid
graph LR; 
A((DELETE));
B[ 'police/' ];
C["{'id':<int:section_id>}"];
A -- REQUEST --> C -->B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns the section in which the police changed to False and all the other attributes of that section

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

**Example**
**PUT   ``` /police/```**
```python
INPUT:
{
	"id":1,
}
OUTPUT:
{
    "id": 1,
    "number_cars": 0,
    "actual_direction": true,
    "n_accident": 0,
    "beginning_coords_x": 0,
    "beginning_coords_y": 0,
    "ending_coords_x": 0,
    "ending_coords_y": 400,
    "street": {
        "name": "Rua Tenente Joaquim Lopes Craveiro",
        "id": 1
    },
    "transit_type": "Normal",
    "police": False,
    "visibility": 50
}
```

## Remove roadblock from a section
```mermaid
graph LR; 
A((DELETE));
B[ 'roadblock/' ];
C["{'id':<int:section_id>}"];
A -- REQUEST --> C -->B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns the following string 'Road Unblocked'

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

**Example**
**Delete   ``` /roadblock/```**
```python
INPUT:
{
	"id":1,
}
OUTPUT:
'Road unblocked'
```


## Remove a accident from a section

```mermaid
graph LR; 
A((DELETE));
B[ 'accident/' ];
C["{'id':<int:section_id>}"]
A -- REQUEST --> C --> B
```

**Possible HTTP Responses**

 > **HTTP_200_OK** -> Returns the following string "Accident removed from section"

 > **HTTP_400_BAD_REQUEST**

 > **HTTP_404_NOT_FOUND**

 > **HTTP_304_NOT_MODIFIED** -> Returns a string with the following message "Currently,there are no accidents in this section"

**Example**
**DELETE   ``` /accident/```**
```python
INPUT:
{
    "id":1,
}
OUTPUT:
"Accident removed from section"
```

**Bad example**

**Section 2 has no accidents at the moment**

**DELETE   ``` /accident/```**
```python
INPUT:
{
    "id":2,
}
OUTPUT:
"Currently,there are no accidents in this section"
```