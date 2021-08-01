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
    #Open DB connection
    database = sqlite3.connect('data.db')

    #Creating a cursor object using the cursor() method
    cursor = database.cursor()

    #Retrieving data
    cursor.execute("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 1;")

    #Fetching the result
    data = cursor.fetchall();
    print(data)
    return jsonify({'num' : "{0:0.1f} °C".format(data[0][2])}, {'timestamp' : data[0][1]})
    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


# select datetime(timestamp, 'localtime') as timestamp, temperature, humidity from weather;
# SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1;