import logging
import pygame
import subprocess
import requests
import pickle
import private
import os
from Adafruit_IO import Client, Feed


class Comms:

    def __init__(self):

        LOG_LEVEL = logging.INFO
        # LOG_LEVEL = logging.DEBUG
        LOG_FILE = "/home/pi/temppi/log_temppi.log"
        LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)

        logging.info('comms init complete')
        pygame.mixer.init()
        self.aio = Client(private.AIO_KEY)

    # PICKLE
    def save_obj(self, obj, name):
        logging.info("Saving " + name)
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/obj/' + name + '.pkl', 'wb') as f:
                pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        except Exception as ee:
            logging.error("Error saving object " + name + ee.__str__())

    def load_obj(self, name):
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/obj/' + name + '.pkl', 'rb') as f:
                return pickle.load(f)
        except Exception as ee:
            logging.error("Error loading object " + name + ee.__str__())
            return None

    # ADAFRUIT.IO
    def aio_send(self, feed, msg):
        try:
            self.aio.send(feed, msg)
        except Exception as ee:
            logging.error("Failed to send to AIO: " + msg + ee.__str__())
            return

    def aio_create_feed(self, feed):
        try:
            self.aio.create_feed(feed)
        except Exception as ee:
            logging.error("Failed to create feed: " + ee.__str__())
            return

    #  IFTTT
    def ifttt(self, val1='hello', val2='hello', val3='hello'):
        try:
            payload = "{ 'value1' : %s, 'value2' : %s, 'value3' : %s}" % (val1, val2, val3)
            requests.post("https://maker.ifttt.com/trigger/wakeup/with/key/" + private.MAKER_SECRET, data=payload)
        except Exception as ee:
            logging.error("Failed to post to IFTTT: " + ee.__str__())
            return

    #  AUDIO
    def play_fx(self, file, loop=0):
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(loop)
        except Exception as ee:
            logging.error("Play sound fx failed: " + ee.__str__())
            return

    def play_speech(self, text):
        try:
            bash_command = "echo '" + text + "' | festival --tts"
            subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        except Exception as ee:
            logging.error("Playing festival tts failed: " + ee.__str__())
            return

