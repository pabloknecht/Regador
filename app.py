from flask import Flask, flash, redirect, render_template, request, session, jsonify
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

#Open DB connection
database = sqlite3.connect('data.db')

#Creating a cursor object using the cursor() method
cursor = database.cursor()

#define get data method
def getHistData(samples):
    cursor.execute("SELECT datetime(timestamp, 'localtime') as timestamp, temperature, humidity FROM weather ORDER BY timestamp DESC LIMIT = ?;", samples)
    data = cursor.fetchall()

    dates = []
    temps = []
    hums = []

    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])
    return dates, temps, hums


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
    #Retrieving data
    cursor.execute("SELECT datetime(timestamp, 'localtime') as timestamp, temperature, humidity FROM weather ORDER BY timestamp DESC LIMIT 1;")

    #Fetching the result
    data = cursor.fetchall();
    print(data)
    temperature = "{0:0.1f} *C".format(data[0][1])
    humidity = "{0:0.1f} %".format(data[0][2])
    timestamp = data[0][0]
    return jsonify({'temperature' : temperature, 'timestamp' : timestamp, 'humidity' : humidity})

"""""   
@app.route("/history", methods=["POST", "GET"])
def history():
    if request.method == "GET":
        dates, temps, hums = getHistData(8640)
        ys = temps
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title("Temperature [*C]")
        axis.set_xlabel("Samples")
        axis.grid(True)
        xs = range(numSamples)
        axis.plot(xs, ys)
        canvas = FigureCanvas(fig)
        output = io.BytesIO()
        canvas.print_png(output)
        response = make_response(output.getvalue())
        response.mimetype = 'image/png'
        return response
        #return render_template("history.html")
"""



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


# select datetime(timestamp, 'localtime') as timestamp, temperature, humidity from weather;
# SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1;