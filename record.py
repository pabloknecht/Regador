import Adafruit_DHT as dht
import time
import sqlite3

def main():
    #Set DATA pin for DHT sensor
    pinDHT = 4

    #Open DB connection
    database = sqlite3.connect('data.db')

    while True:
        #Read Temp and Hum from DHT22
        h,t = dht.read_retry(dht.DHT22, pinDHT)

        #Print Temperature and Humidity on Shell window
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))

        #Register value to database
        database.execute("INSERT INTO weather (timestamp, temperature, humidity) VALUES (CURRENT_TIMESTAMP, ?, ?)", (t, h))
        database.commit()

        #Verify the row count and delete the old
        cursor = database.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather")
        result = cursor.fetchall()
        if result[0] > 3153600:
            print("1 year of data")
        
        time.sleep(10) #Wait 10 seconds and read again

if __name__ == "__main__":
    main()