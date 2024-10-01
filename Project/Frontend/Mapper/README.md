# Traffic Jammer Documentation

## Web Application
For the web development we chose to go with React since one of our developers already had some experience with the technology and there's plenty of modules that could help us achieve what we wanted to do.  

### TrafficWeb (View Traffic)
One of the biggest challenges we faced while going for basic HTML with JavaScript was that the Canvas element wasnt enough, since with canvas we couldn't draw dynamic lines and once we updated the colors, all the canvas would change. 
So we came up with a crafty solution: Using a library called [Konva.js](https://konvajs.org/) we were able to draw multiples lines (with customizable parameters) in a personalized canvas. This allowed us to draw dynamic maps according to the information we got from the server, and repopulate the canvas every X seconds so we could see *real time* changes to the map.

Keypoints for implementation:
 * Dynamic map creation using an algorithm
 * Real time map view
 * Tracking specific cars
 * Allow the user to search multiple cities

### Dashboard (View traffic data)
For the dashboard we can have several options that help us with viewing relevant data concerning each city's streets. This data is viewed through a typical display of number, but also through a chart made using [ChartJS](https://www.chartjs.org/)  
These parameters are customizable:
 * City
 * Street
 * Start Date
 * End Date
 * Week day

### Administration
In the administration page we are able to create a new street, if it passes all needed requirements, which are:  
 * Being in an available city
 * Having a unique name
 * Having beginning coordinates differ from the ending

In the future, we intend for an administrator to also be capable of doing some editing in the sections of the streets, e.g. directly tell the system if a road is blocked, or if there is police activity. Even thought these variables are provided real time by the sensors

## Mobile Application
We inteded to create a mobile application that would display the maps and would send push notifications if the traffic nearby was rapidly increasing. But, the core of the project was made using a library that wasnt present in ReactNative, and so, we had to pushback our changes in mobile and focus on the website.