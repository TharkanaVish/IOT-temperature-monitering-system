import time
import RPi.GPIO as GPIO
import adafruit_dht
import psutil
import check_range
import random
import mqtt

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(4)

while True:
    try:

        temp = sensor.temperature
        humidity = sensor.humidity

        v = random.randint(15,40)
        #publish the value
        mqtt.publish(v)

        #print currnt temperature
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))

        #rotate servo motor through
        check_range.function(v)
        time.sleep(0.5)

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error
    time.sleep(2.0)
