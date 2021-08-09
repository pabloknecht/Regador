from flask import Flask, render_template, request, jsonify, request
import sqlite3
import datetime

# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

#define get data method
def getHistData(startDate, duration):

    #Open DB connection
    database = sqlite3.connect('data.db')
    cursor = database.cursor()

    #Process the function parameters
    startDate = str(startDate)
    endDate = (datetime.datetime.strptime(startDate, '%Y-%m-%d %H:%M') + datetime.timedelta(hours=int(duration))).strftime('%Y-%m-%d %H:%M')
    print("#######################################")
    print("startDate = ", startDate)
    print("endDate = ", endDate)

    #Querry the data
    #cursor.execute("SELECT datetime(timestamp, 'localtime') as timestamp, temperature, humidity FROM weather WHERE timestamp >= \'{}\' AND timestamp <= \'{}\' ORDER BY timestamp DESC;".format(startDate, endDate))
    #cursor.execute("SELECT datetime(timestamp, 'localtime') as timestamp, temperature, humidity FROM weather WHERE timestamp >='2021-08-08 10:00' AND timestamp <='2021-08-08 11:00' ORDER BY timestamp DESC;")
    cursor.execute("SELECT datetime(timestamp, 'localtime') as timestamp, temperature, humidity FROM weather"
                   "WHERE timestamp >=?  AND timestamp <=? ORDER BY timestamp DESC;", (startDate, endDate))
    data = cursor.fetchall()

    dates = []
    temps = []
    hums = []

    print("SELECT datetime(timestamp, 'localtime') as timestamp, temperature, humidity FROM weather WHERE timestamp >= \'{}\' AND timestamp <= \'{}\' ORDER BY timestamp DESC;".format(startDate, endDate))
    print("dates = ", dates)
    print("###########################")

    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])

    database.close()

    return dates, temps, hums
    

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

  
@app.route("/history", methods=["GET"])
def history():

    #getting today and yesterday date
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)

    # 24h of standard duration of the request
    standardPeriod = 24

    #processing date and time formats
    date = request.args.get('date', yesterday.strftime("%Y-%m-%d"))
    time = request.args.get('time', yesterday.strftime("%H:%M"))
    timestamp = date + " " + time
    period = request.args.get('period', str(standardPeriod))

    print("date =", date)
    print("time =", time)
    print("period =", period)
    print("timestamp =", timestamp)

    #Get data
    dates, temperature, humidity = getHistData(timestamp, period)
    return render_template("history.html", dates = dates, temperature = temperature, humidity = humidity)

    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


# select datetime(timestamp, 'localtime') as timestamp, temperature, humidity from weather;
# SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1;