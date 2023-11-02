import sys
import random
import requests
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
BTN_PIN = 11
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
previousStatus = None


'''
global variables
'''
ENDPOINT = "industrial.api.ubidots.com"
DEVICE_LABEL = "pi_huan"
VARIABLE_LABEL = "temperature"
TOKEN = "..."  # replace with your TOKEN
DELAY = 1  # Delay in seconds


def getValue():
    URL = "http://{}/api/v1.6/devices/{}/{}/lv".format(
        ENDPOINT, DEVICE_LABEL, VARIABLE_LABEL)
    HEADERS = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    try:
        attempts = 0
        status_code = 400
        while status_code >= 400 and attempts < 5:
            req = requests.get(url=URL, headers=HEADERS)
            status_code = req.status_code
            attempts += 1
            time.sleep(1)
        return req.text
    except Exception as e:
        print("[ERROR] Error posting, details: {}".format(e))


def post_var(payload, url=ENDPOINT, device=DEVICE_LABEL, token=TOKEN):
    try:
        url = "http://{}/api/v1.6/devices/{}".format(url, device)
        headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

        attempts = 0
        status_code = 400

        while status_code >= 400 and attempts < 5:
            print("[INFO] Sending data, attempt number: {}".format(attempts))
            req = requests.post(url=url, headers=headers,
                                json=payload)
            status_code = req.status_code
            attempts += 1
            time.sleep(1)

        print("[INFO] Results:")
        print(req.text)
    except Exception as e:
        print("[ERROR] Error posting, details: {}".format(e))


def main():
    # Simulates sensor values
    sensor_value = 0

    while True:
        input = GPIO.input(BTN_PIN)
        if input == GPIO.LOW and previousStatus == GPIO.HIGH:
            print("Button pressed @", time.ctime())
            sensor_value = int(float(getValue()))+1
            sensor_value %= 2
            payload = {VARIABLE_LABEL: sensor_value}
            post_var(payload)
        previousStatus = input

    # Sends data


if __name__ == "__main__":
    if TOKEN == "...":
        print("Error: replace the TOKEN string with your API Credentials.")
        sys.exit()
    while True:
        main()
        time.sleep(DELAY)
