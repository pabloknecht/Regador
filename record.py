import Adafruit_DHT as dht
import time
import sqlite3

def main():
    #Set DATA pin for DHT sensor
    database = sqlite3.connect('data.db')
    pinDHT = 4

    while True:
        #Read Temp and Hum from DHT22
        h,t = dht.read_retry(dht.DHT22, pinDHT)

        #Print Temperature and Humidity on Shell window
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))

        #Register value to database
        database.execute("INSERT INTO weather (timestamp, temperature, humidity) VALUES (CURRENT_TIMESTAMP, ?, ?)", (t, h))

        time.sleep(10) #Wait 5 seconds and read again

if __name__ == "__main__":
    main()