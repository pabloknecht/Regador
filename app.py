from flask import Flask, flash, redirect, render_template, request, session
import Adafruit_DHT as dht
from time import sleep

# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


#Set DATA pin
DHT = 4
while True:
    #Read Temp and Hum from DHT22
    h,t = dht.read_retry(dht.DHT22, DHT)
    #Print Temperature and Humidity on Shell window
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))
    sleep(5) #Wait 5 seconds and read again

@app.route('/')
def index():

    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')