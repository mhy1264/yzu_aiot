# Origin : http://blog.miguelgrinberg.com/post/video-streaming-with-flask

from flask import Flask, render_template, Response
from camera_pi import Camera
import RPi.GPIO as GPIO
import sys
import time

previousStatus = None
BUTTON_PIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('stream.html')


def gen(camera):
    nc = 0
    while True:
        input = GPIO.input(BUTTON_PIN)
        if input == GPIO.LOW and previousStatus == GPIO.HIGH:
            mystate = GPIO.LOW
            print("Button pressed @", time.ctime())
            nc += 45
            nc %= 360
        previousStatus = input

        frame = camera.get_frame(nc)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/rotate_image')
def rotate_image():
    if mystate == GPIO.LOW:
        gen(Camera())


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)


