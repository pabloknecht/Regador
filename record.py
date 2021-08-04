import Adafruit_DHT as dht
import time
import sqlite3

def main():
    #Set DATA pin for DHT sensor
    pinDHT = 4

    #Open DB connection
    database = sqlite3.connect('data.db', 8)
    database.execute("PRAGMA journal_mode=WAL")

    while True:
        firstReading = True

        #Read Temp and Hum from DHT22
        h,t = dht.read_retry(dht.DHT22, pinDHT)
        
        if not firstReading:
            #Print Temperature and Humidity on Shell window
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))

            #Register value to database
            database.execute("INSERT INTO weather (timestamp, temperature, humidity) VALUES (CURRENT_TIMESTAMP, ?, ?)", (t, h))
            database.commit()
            database.close()
            time.sleep(60) #Wait 60 seconds and read again
        else:
            firstReading = False


if __name__ == "__main__":
    main()