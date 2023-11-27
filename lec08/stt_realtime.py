import speech_recognition as sr
import RPi.GPIO as GPIO
import time

from gtts import gTTS
import os

tts = gTTS(text='開燈', lang='zh-TW')
tts.save('open.mp3')
tts = gTTS(text='關燈', lang='zh-TW')
tts.save('close.mp3')

LED_PIN = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(LED_PIN, 100)
pwm.start(0)




#obtain audio from the microphone
r=sr.Recognizer()
while 1==1:
        
    with sr.Microphone(device_index = 2, sample_rate = 48000) as source:
        print("Please wait. Calibrating microphone...")
        #listen for 1 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=1)
        # r.energy_threshold = 4000
        print("Say something!")
        audio=r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        print("Google Speech Recognition thinks you said:")
        results = r.recognize_google(audio, language='zh-TW')
    #    results = r.recognize_google(audio, language='en-US')
        print(results)

        if ("開燈" in results):
            pwm.ChangeDutyCycle(100)
            os.system('omxplayer -o local -p open.mp3 > /dev/null 2>&1')
        elif ("關燈" in results):
            pwm.ChangeDutyCycle(0)
            os.system('omxplayer -o local -p close.mp3 > /dev/null 2>&1')

            
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("No response from Google Speech Recognition service: {0}".format(e))
        
