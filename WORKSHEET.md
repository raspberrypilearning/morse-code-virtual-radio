## Introduction: what is Morse Code?

![](./images/qst_may_1942.png)

Invented by [Samuel Morse](http://en.wikipedia.org/wiki/Samuel_F._B._Morse) in the year 1836, Morse Code is a method for sending and receiving text messages using short and long beeps. Conventionally a short beep is called a *dot* and a long one is a *dash* (also known as a *dit* and a *dah*). Every letter of the alphabet has a unique sequence of dots and dashes.

If you look at the chart below, the letter **A** is beep beeeeeep.

The letter **B** is beeeeeep beep beep beep.

![](./images/morse.png)

- A dash is three times the length of a dot
- Each dot or dash has a short gap of silence after it
- Letters in a word have a slightly longer gap of silence between them
- Words have an even longer gap of silence between them

You don't necessarily need to use sound for this, although this is the most common way Morse Code was used. You can do it with anything that can be turned on and off. You could use a torch, raising and lowering a flag or even just blink your eyes fast and slow. This makes it one of the most versatile forms of telecommunication. There is even a formal international treaty which enshrines the Morse code for SOS `... --- ...` (Save Our Souls) as a universal distress signal.

In the 1890's morse code was adapted for use with early [radio](http://en.wikipedia.org/wiki/Radio_communication) before it was possible to send and recieve voice. It was done by simply sending pulses of a carrier wave at an agreed frequency. The recipients radio would then just play an audible tone whenever the carrier was received. It was used extensively during both World Wars and is still used to this day by amateur radio operators.

So there are three aspects to Morse
  - Knowing the code
  - Being able to key it in
  - Being able to decode it when listening

The choice of the dot and dash sequence for each letter is not random. Samuel Morse chose them based on how often letters occurred in the English language used by his local newspaper. The more commonly used a letter was the fewer dots and dashes he chose, thereby making it faster to key in.

The chart below is the Morse code tree and is really helpful when listening/decoding, you might want to print it out and have it always in front of you. You can see that **E** and **T** are the most common letters. So you start at the top, go to the *left* if you hear a dot and to the *right* if you hear a dash. You can double check this against the first chart, try it now for the letters **A** and **B**.

![listening](./images/morse_listening.png)

Get a pencil and paper and see how you get on with this: [Listen to slow Morse Code](./sounds/slow_morse.mp3). Don't be intimidated if you find this hard. It's always tricky to start with. As with many things, the more you do it the easier it gets. In this resource we're going to program the Raspberry Pi to help you learn how to do this. You're going to build your own learning tool which will tell you if you're getting it right or not, so let's get set up.

## Step 0: Setting Up your Pi

First check that you have all the parts you need to get your Raspberry Pi set up and working.

- Raspberry Pi
- Micro USB power adaptor
- An SD card with Raspbian already set up through NOOBS
- USB keyboard
- USB mouse
- HDMI cable
- A monitor or TV

### Activity Checklist:

1. Place the SD card into the slot of your Raspberry Pi.
1. Next connect the HDMI cable from the monitor or TV.
1. Plug in the USB keyboard and mouse.
1. Plug in the micro USB power supply.
1. When prompted to login type:

    ```bash
    Login: pi
    Password: raspberry
    ```

## Step 1: Play some test beeps

Headphones are advisable in a classroom environment so that the room doesn't descend into a cacophony of beep noise. If you *are* using headphones or a speaker on the Raspberry Pi, you will need to run the following command to redirect sound to the headphone socket:

`sudo amixer cset numid=3 1`

Next we're going to use the python pygame library to make some tone sounds.
First verify that the package is installed using the following command:

`sudo apt-get install python-pygame -y`

If your SD card is up to date you should see the message:

`python-pygame is already the newest version`

Okay now lets do some programming.  I'm going to provide some code to make the tone sound, you don't need to worry about its internal workings. For those of you that are interested though the code just inherits one of the pygame sound classes and automatically generates the wave data for playing a tone at a specified frequency.

Enter the following command to start editing a blank file:

`nano morse-code.py`

Now either copy and paste or enter the following code:
```python
#!/usr/bin/python
import pygame, time
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
        for time in xrange(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples
```
Don't worry if you've never seen a python [class](http://en.wikipedia.org/wiki/Class_%28computer_programming%29) before. A class is like a blueprint of code that you can re-use multiple times. An instance of a class is known as an [object](http://en.wikipedia.org/wiki/Object-oriented_programming).


Typical Morse Code tones are somewhere between 400 Hz and 1000 Hz, so lets go for 800 Hz.
In this code `tone_obj` is the object that has been created from the blueprint `ToneSound`.
Add the following code to the very bottom of the file:

```python
tone_obj = ToneSound(frequency = 800, volume = .5)

tone_obj.play(-1) #the -1 means to loop the sound
time.sleep(2)
tone_obj.stop()
```
Press *Ctrl - O* then *Enter* to save followed by *Ctrl - X* to quit from editing.
Next mark the file as executable with the following command:

`chmod +x morse-code.py`

Now we can run the code, you should hear a nice two second long beep.

`./morse-code.py`

If you didn't hear anything then double check everything is plugged in correctly. If you're using the headphone jack of the Pi you'll need to use the command `sudo amixer cset numid=3 1` to redirect the audio. You may notice the tone sounds a bit wobbly at the start, this is just an artefact of pygame starting up and using up CPU cycles. Subsequent tones that we make will sound correct.

##Step 2: Wire up the Morse Code key to the GPIO pins

### The Theory

All Morse Code keys work in a similar way to a normal push button. They have a couple of screw terminals for attaching a positive and a negative wire. When you press the key down two bits of metal touch causing a short circuit. The effect would be the same if you just touched the two bare wires together.

So to connect the Morse Key to the GPIO pins we need to do a bit of physical computing. Any GPIO pin can be set up as an input or an output. Output mode is for when you want to supply voltage to something like an LED or a BUZZER. However, input mode is for when you want to detect voltage coming from something. So since we want to detect the key being pressed we're going to use input mode.

When a GPIO pin is in input mode the pin is said to be *floating* meaning that it has no fixed voltage level. That's no good for what we want. We need to categorically know either the key is down or the key is up. So we need to fix the voltage level of the pin so that it is no longer floating. We can do it in to ways:

- A pull up circuit

  Wire the GPIO pin to 3.3 volts through a large 10kΩ resistor so that it always reads HIGH. Then we can short the pin to ground via the Morse Key so that the pin will go LOW when you press it.

  ![](./images/pull_up.png)

- A pull down circuit

  Wire the GPIO pin to ground through a large 10kΩ resistor so that it always reads LOW. Then we can short the pin to 3.3 volts through the Morse key so that it goes HIGH when you press it. When the key is pressed there is a lower resistance path to 3.3 volts and therefore the pin will read HIGH. 

  ![](./images/pull_down.png)
  
  *Note: The 1kΩ resistor is there in both circuits to give the GPIO pin a failsafe protection in case we mistakenly set the pin to be in OUTPUT mode.*

Fortunately the Raspberry Pi has this circuitry **built in** and we can select a pull up or down circuit in our code for each GPIO pin. So you can get away with just using two jumper wires here, although you're welcome to wire it up the proper way shown above if you wish.

### The Practise

- Pull up configuration

  ![](./images/pull_up_key.png) 

- Pull down configuration

  ![](./images/pull_down_key.png) 
