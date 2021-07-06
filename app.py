from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import Adafruit_DHT as dht
import time
import threading
import datetime

# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Set DATA pin for DHT sensor
pinDHT = 4

def readingDHT():
    while True:
        #Read Temp and Hum from DHT22
        global h,t 
        h,t = dht.read_retry(dht.DHT22, pinDHT)
        #Print Temperature and Humidity on Shell window
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))
        time.sleep(5) #Wait 5 seconds and read again

threading.Thread(target=readingDHT).start()


@app.route('/')
def index():

    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')