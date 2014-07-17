#!/usr/bin/python
import pygame, time, RPi.GPIO as GPIO, thread
from array import array
from pygame.locals import *
from morse_lookup import *

pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

class ToneSound(pygame.mixer.Sound):
    def __init__(self, frequency, volume):
        self.frequency = frequency
        pygame.mixer.Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        for time in xrange(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples


tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_keydown(pin):
    while GPIO.input(pin):
        time.sleep(0.01)

def wait_for_keyup(pin):
    while not GPIO.input(pin):
        time.sleep(0.01)
            
def decoder_thread():
    global key_up_time
    global buffer
    global new_word
    global new_letter
    while True:
        time.sleep(.01)
        key_up_length = time.time() - key_up_time
        if new_word and key_up_length >= 4:
            new_word = False
            sys.stdout.write(" ")
            sys.stdout.flush()
        elif new_letter and key_up_length >= 1.50:
            new_letter = False
            if len(buffer) > 0:
                bit_string = "".join(buffer)
                try_decode(bit_string)
                del buffer[:]

DOT = "."
DASH = "-"

key_down_time = 0
key_down_length = 0
key_up_time = 0
buffer = []
new_letter = False
new_word = False

thread.start_new_thread(decoder_thread, ())

while True:
    wait_for_keydown(pin)
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    key_up_time = time.time() #record the time when the key was released
    key_down_length = key_up_time - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    new_letter = new_word = True
    buffer.append(DASH if key_down_length > 0.15 else DOT)
