from flask import Flask, flash, redirect, render_template, request, jsonify, request
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import Adafruit_DHT as dht
import time
import sqlite3
import threading
import datetime



# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

#define get data method
def getHistData(samples):

    #Open DB connection
    database = sqlite3.connect('data.db')
    cursor = database.cursor()
    cursor.execute("SELECT datetime(timestamp, 'localtime') as timestamp, temperature, humidity FROM weather ORDER BY timestamp DESC LIMIT :number;", {"number" : samples})
    data = cursor.fetchall()

    dates = []
    temps = []
    hums = []

    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])

    database.close()

    return dates, temps, hums
    
getHistData(800)
    

def getLastMeasure():
    #Open DB connection
    database = sqlite3.connect('data.db')
    cursor = database.cursor()
    #Retrieving data
    cursor.execute("SELECT datetime(timestamp, 'localtime') as timestamp, temperature, humidity FROM weather ORDER BY timestamp DESC LIMIT 1;")
    #Fetching the result
    data = cursor.fetchall();
    database.close()
    return data


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
        return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = getLastMeasure()
    print(data)
    temperature = "{0:0.1f} *C".format(data[0][1])
    humidity = "{0:0.1f} %".format(data[0][2])
    timestamp = data[0][0]
    return jsonify({'temperature' : temperature, 'timestamp' : timestamp, 'humidity' : humidity})

  
@app.route("/history", methods=["GET", "POST"])
def history():
    if request.method == "GET":
        #Get 1 day of data
        date, temperature, humidity = getHistData(5)
        return render_template("history.html", date = date, temperature = temperature, humidity = humidity)
    else:
        return render_template("history.html")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


# select datetime(timestamp, 'localtime') as timestamp, temperature, humidity from weather;
# SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1;