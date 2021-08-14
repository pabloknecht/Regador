# Temperature and Humidity Monitoring System

This project consists of two parts: a data collection system and a flask application running a webpage where we can visualise the temperature and the humidity in real time or plot this data for a given period of time.
All two parts run in a Raspberry Pi 3 where a humidity and temperature sensor is connected to.

## Data collection system
This application called `record.py`, which is writen in python, register in a SQlite database the measures of the sensor each 60s. The sensor is a DHT 22 and the function used to read it commes from Adafruit, installed with the command:
```
sudo pip3 install Adafruit_Python_DHT
```
The function used is `dht.read_retry(dht.DHT22, pinDHT)`. After the reading the data is registered in the databese with it's timestamp.

## Website Flask
The website is composed by two pages, one showing the temperature and humidity in real time, using a Ajax call, and the other shows the temperature and the humidity for a given period.
The standard starting time and period, when the page is requested by GET is the day before and 24 hours respectively.

### Charts
The charts are created using JS Chart, which can be found here:
`<script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"></script>`

### Date and time
The date and time are managed with strings in the format `'%Y-%m-%d %H:%M'` and by datetime objects as the database uses UTC timezone.

### Ploting data on command

There is a form in the History web page with three inputs:
`<input type="date" id="date" name="date" value="{{pre_date}}">
<input type="time" id="time" name="time" value="{{pre_time}}">
<input type="number" id="period" name="period" value="{{pre_period}}" placeholder="Duration (h)">`

Those inputs are used to get the start date and the period of data desired. This information is transfred by the URL using a GET message. The backend then treats the parameters and retreive the data to be sent back to the front and and ploted by JS Chart

##Conclusion
This projet uses many concepts I learned in the course, like databases, python, GET and POST requests, HTML, etc. But it also uses others like Ajax calls, JS Chart and Raspberry Pi programming.