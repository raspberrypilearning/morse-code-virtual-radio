## Play a test beep

First boot up your Raspberry Pi and log in.

As this exercise involves noise, you should use headphones if you are in a classroom environment, to avoid distracting others around you. If you are using headphones or a speaker on the Raspberry Pi, you will need to run the following command to redirect sound to the headphone socket:

```bash
sudo amixer cset numid=3 1
```

First, we need some code to make the tone sound. Enter the following command to start editing a blank file (please note that you should use Python 3 for this project):

```bash
nano morse-code.py
```

Now either copy and paste or enter the following code:

```python
#!/usr/bin/python3
import pygame
import time
from array import array
from pygame.locals import *

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
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples
```

You don't need to worry about the inner workings of this code, but, if you are interested, the code inherits one of the `pygame` sound classes, and automatically generates the wave data for playing a tone at a specified frequency.

Don't worry if you've never seen a Python [class](http://en.wikipedia.org/wiki/Class_%28computer_programming%29) before. A class is like a blueprint of code that you can re-use multiple times. An instance of a class is known as an [object](http://en.wikipedia.org/wiki/Object-oriented_programming).

Typical Morse Code tones are somewhere between 400 Hz and 1000 Hz; in this project, we will use a frequency of 800 Hz. In this code, `tone_obj` is the object that has been created from the blueprint `ToneSound`.

Add the following code to the very bottom of the file:

```python
tone_obj = ToneSound(frequency = 800, volume = .5)

tone_obj.play(-1) #the -1 means to loop the sound
time.sleep(2)
tone_obj.stop()
```
Press `Ctrl + O` then `Enter` to save followed by `Ctrl + X` to quit.

Next, mark the file as executable with the following command:

```python
chmod +x morse-code.py
```

Now we can run the code; when you do, you should hear a nice two-second-long beep:

```python
./morse-code.py
```

If you didn't hear anything then double-check everything is plugged in correctly. If you're using the headphone jack of the Pi, remember that you'll need to use the command `sudo amixer cset numid=3 1` to redirect the audio. You may notice the tone sounds a bit wobbly at the start; this is just an artefact of `pygame` starting up and using up CPU cycles. Subsequent tones will sound correct.

