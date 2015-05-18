![](images/FWW_Centenary__Led_By_IWM_Red-web.png)

#Morse Code Virtual Radio

This tutorial will show you how to connect a Morse key to the Raspberry Pi GPIO pins, and how to write code to play tones when you hold the key down. You will also decode the Morse that you're keying so that it comes up on the screen.

##What is Morse Code?

![](images/qst_may_1942.png)

Invented by [Samuel Morse](http://en.wikipedia.org/wiki/Samuel_F._B._Morse) in 1836, Morse Code is a method for sending and receiving text messages using short and long beeps. Conventionally, a short beep is called a *dot* and a long one is a *dash* (also known as a *dit* and a *dah*). Every letter of the alphabet has a unique sequence of dots and dashes.

If you look at the chart below, the letter **A** is beep beeeeeep and the letter **B** is beeeeeep beep beep beep.

![](images/morse.png)

- All timings are defined as multiples of one dot length
- A dash is three times the length of a dot
- Each dot or dash has a short gap of silence after it (usually 1 dot length)
- Letters in a word have a slightly longer gap of silence between them (usually 3 dot lengths)
- Words have an even longer gap of silence between them (usually 7 dot lengths)

You don't necessarily need to use sound for this, although this is the most common way Morse Code was used. You can do it with anything that can be turned on and off; this could be a torch, raising and lowering a flag, or even just blinking your eyes quickly and slowly. This makes it one of the most versatile forms of telecommunication. There is even a formal international treaty which enshrines the Morse code for SOS `... --- ...` (Save Our Souls) as a universal distress signal.

In the 1890s Morse Code was adapted for use with early [radio](http://en.wikipedia.org/wiki/Radio_communication) before it was possible to send and receive voice. It was done by simply sending pulses of a carrier wave at an agreed frequency. The recipient's radio would then just play an audible tone whenever the carrier was received. It was used extensively during both World Wars and is still used to this day by amateur radio operators.

There are three essentials to using Morse:

  - Knowing the code
  - Being able to key it in
  - Being able to decode it when listening

The choice of the dot and dash sequence for each letter is not random. Samuel Morse chose them based on how often letters occurred in the English language used by his local newspaper. The more commonly-used a letter was, the fewer dots and dashes he chose, thereby making it faster to key in.

The chart below is the Morse code tree, and is really helpful when listening and decoding; you might want to print it out and keep it in front of you. You can see that **E** and **T** are the most common letters. So you start at the top, go to the *left* if you hear a dot and to the *right* if you hear a dash. You can double-check this against the first chart: try it now for the letters **A** and **B**.

![listening](images/morse_listening.png)

Get a pencil and paper and see how you get on with this: [listen to slow Morse Code](./code/slow_morse.mp3). Don't be intimidated if you find following the code hard; it's always tricky to start with. As with many things, the more you do it the easier it gets.

## Play a test beep

First boot up your Raspberry Pi and log in.

Headphones are advisable in a classroom environment, to avoid distracting others around you. If you *are* using headphones or a speaker on the Raspberry Pi, you will need to run the following command to redirect sound to the headphone socket:

`sudo amixer cset numid=3 1`

First, we need some code to make the tone sound. Enter the following command to start editing a blank file:

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

You don't need to worry about the inner workings of this code, but, if you are interested, the code inherits one of the `pygame` sound classes, and automatically generates the wave data for playing a tone at a specified frequency.

Don't worry if you've never seen a Python [class](http://en.wikipedia.org/wiki/Class_%28computer_programming%29) before. A class is like a blueprint of code that you can re-use multiple times. An instance of a class is known as an [object](http://en.wikipedia.org/wiki/Object-oriented_programming).

Typical Morse Code tones are somewhere between 400 Hz and 1000 Hz, so let's go for 800 Hz. In this code, `tone_obj` is the object that has been created from the blueprint `ToneSound`.

Add the following code to the very bottom of the file:

```python
tone_obj = ToneSound(frequency = 800, volume = .5)

tone_obj.play(-1) #the -1 means to loop the sound
time.sleep(2)
tone_obj.stop()
```
Press `Ctrl - O` then `Enter` to save followed by `Ctrl - X` to quit.

Next, mark the file as executable with the following command:

`chmod +x morse-code.py`

Now we can run the code; when you do, you should hear a nice two-second-long beep:

`./morse-code.py`

If you didn't hear anything then double-check everything is plugged in correctly. If you're using the headphone jack of the Pi, remember that you'll need to use the command `sudo amixer cset numid=3 1` to redirect the audio. You may notice the tone sounds a bit wobbly at the start; this is just an artefact of `pygame` starting up and using up CPU cycles. Subsequent tones that we make will sound correct.

## Connect the Morse Code key to the GPIO pins

All Morse Code keys work in a similar way to a push button or switch. They have two screw terminals for attaching a positive and a negative wire. When you press the key down, two bits of metal touch, causing a circuit to complete. The effect would be the same if you just touched the two wires together.

So to connect the Morse key to the GPIO pins, we need to do a bit of physical computing. GPIO pins can be set up as an input or an output. Output mode is used when you want to supply voltage to a device like an LED or buzzer. If we use input mode, a GPIO pin has a value that we can read in our code. If the pin has voltage going into it, the reading will be `1` (HIGH); if the pin was connected directly to ground (no voltage), the reading will be `0` (LOW). 

So the goal is to use the Morse Code key to switch voltage on and off for a GPIO pin, thus making the reading of the pin change in our code when we press the key.

When a GPIO pin is in input mode the pin is said to be floating, meaning that it has no fixed voltage level. That's no good for what we want, as the pin will randomly float between HIGH and LOW. We need to categorically know that the key is either up or down. So we need to fix the voltage level to HIGH or LOW, and then make it change only when the key is pressed.

We can do this in two ways.

### A pull up circuit

  Wire the GPIO pin to 3.3 volts through a large 10kΩ resistor so that it always reads HIGH. Then we can short the pin to ground via the Morse key, so that the pin will go LOW when you press it.

  ![](images/pull_up.png)

### A pull down circuit

  Wire the GPIO pin to ground through a large 10kΩ resistor so that it always reads LOW. Then we can short the pin to 3.3 volts through the Morse key, so that it goes HIGH when you press it. When the key is pressed there is a lower resistance path to 3.3 volts, and therefore the pin will read HIGH. 

  ![](images/pull_down.png)
  
Note: The 1kΩ R2 resistor is there in both circuits to give the GPIO pin a fail-safe protection, in case we mistakenly set the pin to be in OUTPUT mode.

Fortunately, the Raspberry Pi has all the above circuitry built in and we can select either a pull up or a pull down circuit in our code for each GPIO pin. This sets up some internal circuitry that is too small for us to see. So you can get away with just using two jumper wires here, although you're welcome to wire it up the way shown above if you wish. Let's use pin #7 as an example:

### Pull up configuration

  GPIO pin #7 will be wired to 3.3 volts using the internal pull up resistor, so that it always reads HIGH. Then we can short the pin to ground via the Morse key, so that the pin will go LOW when you press it.

  ![](images/pull_up_key.png) 

### Pull down configuration

  GPIO pin #7 will be wired to ground using the internal pull down resistor, so that it always reads LOW. Then we can short the pin to 3.3 volts via the Morse key, so that the pin will go HIGH when you press it.

  ![](images/pull_down_key.png) 

Both methods will work equally well; which one people use is often just personal preference. Take the two jumper wires and screw the male ends into the terminal blocks on your Morse Code key. On some very old antique keys this can be a tricky operation.

![](images/jumper_wires_key.png) 

Choose the pull up or down configuration you want to use and connect the female ends to the appropriate GPIO pins on your Raspberry Pi; use the above diagrams as a guide. **Make a note of which configuration you're using as you'll need to incorporate it into your programming later**.

## Detect the key position through the GPIO pin value

Enter the following command to edit our previous tone program:

`nano morse-code.py`

To give us access to the GPIO pins in our code, we need to import the `RPi.GPIO` library.
Add `RPi.GPIO as GPIO` to the `import` line at the top so that it reads:

`import pygame, time, RPi.GPIO as GPIO`

At the bottom remove these lines (they will be put back in again later):

```python
tone_obj.play(-1)
time.sleep(2)
tone_obj.stop()
```

Either copy and paste or enter the code below. Pay attention to the `GPIO.setup` command. This line is doing two things: it is setting pin 7 as an input, *and* setting the internal pull up resistor on it. If you want to use the pull down resistor, you'll need to use `GPIO.PUD_DOWN` instead.

There is then a `while` loop, which continually reads the state of pin 7 and prints HIGH or LOW to the screen every second.

```python
pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    reading = GPIO.input(pin)
    print "HIGH" if reading else "LOW"
    time.sleep(1)
```

Press `Ctrl - O` then `Enter` to save followed by `Ctrl - X` to quit.

GPIO functions require root access on your Pi, so from now on you must use the `sudo` command to run your code. If you don't use `sudo` you'll see the following error: `No access to dev/mem. Try running as root!`

`sudo ./morse-code.py`

If you're using a pull up, the program should show HIGH when the key is up. Hold the button down for a few seconds and it will show LOW. It will be the opposite way around if you're using a pull down. The output should look something like this:

```bash
HIGH
HIGH
HIGH
LOW
LOW
LOW
HIGH
HIGH
HIGH
```

Press `Ctrl - C` to quit.

## Play a tone when the key is down

We've now proven that the value of the GPIO pin is changing when we press the Morse key, so the electronics is done. But our code is still very basic. All we have is a loop that keeps polling the pin; the code doesn't actually respond to the press or release of the key yet. You'll notice that you can press and release the key many times within one second.

To do Morse Code properly, we need to respond every time the user presses or releases the key, by starting and stopping the tone sound.

**TIP**: The more experienced people reading this will be thinking about using hardware interrupts here. This is done in the `RPi.GPIO` library with the `add_event_detect` and `wait_for_edge` functions. **Do not rush ahead and do this.** The use of hardware interrupts is problematic here. You will find that after some vigorous button bashing it cannot distinguish between a rising or falling edge, and your tone will play at the wrong times.

The most reliable way to do this with the `RPi.GPIO` library is to write a couple of functions which hold up the execution of your code until the key has been pressed or released. The overall goal here would be the following algorithm:

- Loop
  - Wait for key down
  - Start playing tone
  - Wait for key up
  - Stop playing tone

We can do this by defining two functions called `wait_for_keyup` and `wait_for_keydown`. These functions will use a `while` loop that will make the Pi sleep until the pin state has changed. You need to be mindful of the pull up or down configuration you're using. For example, if you're using a pull up, the logic in the `wait_for_keydown` function will be *while pin 7 is HIGH keep sleeping*; so while the key is up, the pin will be HIGH. When the key is pressed the pin goes LOW, and we can stop sleeping and start playing the tone. For a pull down, however, the logic would be *while pin 7 is LOW keep sleeping*. In order to have a good response time, we only need to sleep for a very short amount of time for each iteration of the loop. One hundredth of a second is ideal (0.01 seconds).

The `wait_for_keyup` function will then be the same but will have the opposite logic to whatever is in `wait_for_keydown`.

Have a look at the code below. This is for a pull up configuration; if you're using pull down your `GPIO.setup` line will have `GPIO.PUD_DOWN`, and you would just need to move the `not` keyword from `wait_for_keyup` into the same place in `wait_for_keydown`.

```python
def wait_for_keydown(pin):
    while GPIO.input(pin):
        time.sleep(0.01)
	
def wait_for_keyup(pin):
    while not GPIO.input(pin):
        time.sleep(0.01)

tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "Ready"

while True:
    wait_for_keydown(pin)
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    tone_obj.stop()
```

Enter the following command to edit our previous program:

`nano morse-code.py`

Leave the `ToneSound` class at the top of your program, scroll to the bottom, delete the previous `while` loop code and then add the code above. If necessary, modify it for a pull down configuration.

Press `Ctrl - O` then `Enter` to save followed by `Ctrl - X` to quit.

You can now test your code. Remember to use the `sudo` command.

`sudo ./morse-code.py`

After the you see the `Ready` message you should be able to start doing your first Morse Code messages. Give the key a good test to make sure that the tone is only ever on when the key is down, and off when the key is up. If you've got it the wrong way around check the logic in your `wait_for_keyup` and `wait_for_keydown` functions. You may just need to move the `not` keyword.

Now have a go at a short word. Early Nokia mobile phones used the Morse Code for SMS when a text message arrived. This is a really easy one to do; the Morse Code for SMS is `... -- ...`, and feel free to Google *nokia sms tone* to double-check. Try other words using the chart at the top.

Press `Ctrl - C` to quit.

## Decode the Morse as you go

What will really help you learn is having a way to know when you're getting the code right or wrong. We can program the Pi to decode what you're keying in and then print the letters to the screen as you go. With this you can pick a message, try to key it in and immediately see if the correct text is being displayed. If the wrong text comes up then it's likely that you didn't key in the correct Morse Code sequence. Practice makes perfect!

Here is an example [video](https://www.youtube.com/watch?v=P7BT7aI1BPg).

To program this, we should remind ourselves about the rules of International Morse Code:

- All timings are defined as multiples of one dot length
- A dash is three times the length of a dot
- Each dot or dash has a short gap of silence after it (usually 1 dot length)
- Letters in a word have a slightly longer gap of silence between them (usually 3 dot lengths)
- Words have an even longer gap of silence between them (usually 7 dot lengths)

So to start with, we need to tell the difference between a dot and a dash. We can do that by timing how long the key is held down for to give us the length of the tone. Then we need to tell the difference between the dots and dashes making up one word and the next. To do *that* we can time how long the key is up for, so we're measuring the gap of silence between the tones. The same measurement of time will also give us the difference between letters making up a word and separate words.

### Distinguish dot and dash

Let's firstly program the Pi to recognise the difference between a dot and a dash.

The aim is to time how long the key is held down for. Generally speaking, a dot is about 0.15 seconds or less and anything longer than this is a dash. You're welcome to use a different value if you wish but I recommend 0.15. The way to time something in code is to record the time now, wait until something has happened and then subtract the time you recorded from the current time.

Take a look at the code below; notice the the use of the `key_down_time` and `key_down_length` variables.

```python
def wait_for_keydown(pin):
    while GPIO.input(pin):
        time.sleep(0.01)
	
def wait_for_keyup(pin):
    while not GPIO.input(pin):
        time.sleep(0.01)

tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DOT = "."
DASH = "-"

key_down_time = 0
key_down_length = 0

print "Ready"

while True:
    wait_for_keydown(pin)
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    key_down_length = time.time() - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    
    if key_down_length > 0.15:
        print DASH
    else:
        print DOT
```

Enter the following command to edit our previous program:

`nano morse-code.py`

Scroll to the bottom and add the lines shown above that are missing from your code. If necessary, modify it for a pull down configuration. When you're done press `Ctrl - O` then `Enter` to save followed by `Ctrl - X` to quit. You can now test your code. Remember to use the `sudo` command.

`sudo ./morse-code.py`

Use the Morse key to make some long and short tones. You should see dots and dashes appearing at the moment when you release the key. The output will look something like this:

```
.
.
.
-
-
.
.
.
```

Press `Ctrl - C` to quit.

### Translate into text

Next, we need a way to combine these dots and dashes to form letters and words. This is actually a little more tricky than it sounds. Consider how we're going to know when the user has finished a letter and when they have finished a word. The correct behaviour will be the following:

- When they finish a letter, display the *letter*
- When they finish a word, display a *space character*

I am going to provide some code to make this easier. This code will allow you to take a string of dots and dashes and look up the corresponding letter of the alphabet. Enter the following command to download this code:

`wget https://raw.githubusercontent.com/raspberrypilearning/morse-code/master/morse_lookup.py --no-check-certificate`

Now let's have a quick look at it. Enter the command below to edit the file:

`nano morse_lookup.py`

The `morse_code_lookup` variable is a Python *dictionary* object. A dictionary works using keys and values; for every key there is a corresponding value. You could create a dictionary to translate between, say, English and French. The key could be *Hello* and the value would be *Bonjour*. Look at the code below as an example:

```python
english_to_french = {
    "Hello": "Bonjour",
    "Yes": "Oui",
    "No": "Non"
    }
    
print english_to_french["Hello"]
```

The result of the above code would be: `Bonjour`.

We're going to use this technique to translate between the sequence of dots and dashes and their corresponding letter. For example, `-.-.` is the letter `C`. The `try_decode` function at the bottom can be used to check that a dot-dash sequence is valid and, if so, translate it into the corresponding letter.

Press `Ctrl - X` to quit from editing without saving.

### Multithreading concept

I need to introduce a new programming concept called [multithreading](http://en.wikipedia.org/wiki/Multithreading_%28software%29#Multithreading). A *thread* in a program is a single sequence of instructions that are being followed by the computer at any one time. In most simple programs there is only one thread, which is the main one. But it is possible to have multiple threads going at the same time; it's like making a program pat its head and rub its belly at the same time.

Because our main thread is always held up by the `wait_for_keydown` and `wait_for_keyup` functions, we need to have another thread which can constantly do the work of decoding what the user is keying in.

The overall goal here will be to modify the main *thread* so that it stores every dot and dash in a buffer list. The decoder *thread* will then be watching independently for different lengths of silence. If it's a short gap of silence then that’s a new letter, so it will use the `try_decode` function to see if the buffer contents matches a letter; it will also empty the buffer, ready for the next word. If the gap of silence gets longer, then it's a new word and we should show a space character.

### Add the code

Now lets go back to editing our main program. Enter the following command:

`nano morse-code.py`

Firstly, we need to add two new variables. `key_up_time` is to record when the key was released so that the length of silent gaps can be measured in our code. The other is called `buffer`; this is a list which will temporarily hold the dots and dashes before a full word is complete.

```python
key_up_time = 0
buffer = []
```

Add these variables to your code as shown below. There are also two new lines to add inside the main `while` loop: a line which sets `key_up_time`, and another that appends to the `buffer` list. Make sure you add both of them.

```python
key_down_time = 0
key_down_length = 0
key_up_time = 0
buffer = []

print "Ready"

while True:
    wait_for_keydown(pin)
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    key_up_time = time.time() #record the time when the key was released
    key_down_length = time.time() - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    buffer.append(DASH if key_down_length > 0.15 else DOT)
```

Double-check that your code is the same as the above. When you're done, press `Ctrl - O` then `Enter` to save. We're not finished editing yet though; do not run the code as it is. We still need to add code for the new *thread*.

First we need to add some new imports to the top of our file. Scroll up to the top and find the `import` line. We need to add `thread` to do multithreading and `from morse_lookup import *` to give us access to the lookup code we downloaded earlier. The code should now look like this:

```python
#!/usr/bin/python
import pygame, time, RPi.GPIO as GPIO, thread
from array import array
from pygame.locals import *
from morse_lookup import *
```

Next, let's put in the code that will run on our separate *thread*. To do this, you can just define a function and this will be what is run *on* that thread. Add this function to your code just below the `wait_for_keyup` function:

```python
def decoder_thread():
    global key_up_time
    global buffer
    new_word = False
    while True:
        time.sleep(.01)
        key_up_length = time.time() - key_up_time
        if len(buffer) > 0 and key_up_length >= 1.5:
            new_word = True
            bit_string = "".join(buffer)
            try_decode(bit_string)
            del buffer[:]
        elif new_word and key_up_length >= 4.5:
            new_word = False
            sys.stdout.write(" ")
            sys.stdout.flush()
```

Let's go through this. The first thing you'll notice is the use of the `global` keyword. This will give the thread access to the `key_up_time` and `buffer` variables that belong to the main thread, so that they can be used here. Next, we have a variable called `new_word`. Once the end of the word has been detected we set this to `False`, so that we don't keep putting more spaces down.

We then have another `while True` loop; the main purpose of this is to continually monitor the gaps of silence between tones. You'll see there is a `sleep` command to avoid overloading the CPU; then we calculate the `key_up_length`, which is the `key_up_time` from the main thread subtracted from the current time. Every time around the loop, which is every 0.01 seconds, the `key_up_length` value will increase as long as the Morse key stays up.

Next is an `if` statement. There are two conditions upon which we need to act here:

1. The first condition is when there is something in the `buffer` and the gap of silence is big enough to mean a new letter. We're hard-coding the value of `1.5` seconds for this. If this situation happens we know we're in a new word, so we set the `new_word` variable to `True`. The line `bit_string = "".join(buffer)` is taking the dots and dashes in the `buffer` list, and turning them into a single string that might be something like `.-..`. We can then see if that matches a key in the Morse translation dictionary via the `try_decode` function. The `try_decode` function displays the result. We then empty the buffer, ready for the next word, with `del buffer[:]`. If we didn't do this, the buffer would just get bigger and bigger, and would never match any letters in the `morse_lookup.py` dictionary.

1. The second condition is when the gap of silence has increased to `4.5` seconds. Remember a rule of Morse is that the gap of silence for a new word has to be three times the length that means a new letter: `1.5 x 3 = 4.5`. So here we just set `new_word` to False, so that the `else if` condition no longer succeeds, and then put down a space character.

*Note:* The use of `sys.stdout` is so that we can print to the screen without having to always show a new line, as with the default `print` command.

The choice of `1.5` and `4.5` seconds is essentially arbitrary, but they are about right for someone who is new to Morse and will be going quite slowly. As your skill improves, you may wish to reduce these numbers in your code. This will allow you to key in the code faster, but it also demands a greater level of skill from you. I can cope with 0.75 and 2.25 seconds respectively and I am sure there are ex-telegraph operators out there that could have these values much lower!

Press `Ctrl - O` then `Enter` to save. There is one more thing we need to do before we can run our code, which is to add a line of code that will *launch* the new thread. This has to be done from the *main thread*, so scroll down and find the `print "Ready"` line. Add the line below just before it:

`thread.start_new_thread(decoder_thread, ())`

The **final code** should look like this; remember to make the necessary changes if you're using a pull down instead of up. Do one last check:

```python
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

def wait_for_keydown(pin):
    while GPIO.input(pin):
        time.sleep(0.01)

def wait_for_keyup(pin):
    while not GPIO.input(pin):
        time.sleep(0.01)

def decoder_thread():
    global key_up_time
    global buffer
    new_word = False
    while True:
        time.sleep(.01)
        key_up_length = time.time() - key_up_time
        if len(buffer) > 0 and key_up_length >= 1.5:
            new_word = True
            bit_string = "".join(buffer)
            try_decode(bit_string)
            del buffer[:]
        elif new_word and key_up_length >= 4.5:
            new_word = False
            sys.stdout.write(" ")
            sys.stdout.flush()

tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DOT = "."
DASH = "-"

key_down_time = 0
key_down_length = 0
key_up_time = 0
buffer = []

thread.start_new_thread(decoder_thread, ())

print "Ready"

while True:
    wait_for_keydown(pin)
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    key_up_time = time.time() #record the time when the key was released
    key_down_length = key_up_time - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    buffer.append(DASH if key_down_length > 0.15 else DOT)
```
When you're done press `Ctrl - O` then `Enter` to save followed by `Ctrl - X` to quit. You can now test your code. Remember to use the `sudo` command.

`sudo ./morse-code.py`

Wait for the `Ready` message to show and then begin. *TIP:* The trick is to watch the screen and wait for a letter to appear before you start keying in the next one. You may wish to refer to the charts at the top of this page.

SOS is `...` `---` `...`

Hello is `....` `.` `.-..` `.-..` `---`

The output should look like this:

`SOS HELLO `

Press `Ctrl - C` to quit.

You can ignore the message saying `Unhandled exception in thread`; this is just the child thread being terminated when you send the `KeyboardInterrupt` with `Ctrl - C`.

## Play a listening game with a friend

![](images/decoding.png)

Now that you have a way to verify the correctness of your keying, you can play a listening game with a friend.

The other person should:

- Have a printout of the Morse code tree
- Some paper, a pencil, and an eraser
- Be able to hear your Morse tones
- Not be able to see your screen

The aim of the game is to key in a message and see if the other person can decode it using just their ears. This is how it was done during both World Wars. It's trickier than it sounds so go slowly and start off with just letters, then progress onto words and messages. The other person should write down on some paper what they think is being keyed in; when the message is finished you can compare what they wrote down to what was shown on the screen.

*TIP:* Try not to write dots and dashes; instead try to get into the zone of listening to the tones, following the tree and arriving at a letter. Write down letters!

*TIP:* If the message sounds like gibberish when you're decoding just keep going; the person behind the screen could be making mistakes. The aim is for you to have exactly what is shown on their screen, even if it's wrong!

Good luck!

## What next?

One of the things you may wish to do is extend the decoding ability of this project to include punctuation characters like the full stop `.-.-.-`, comma `--..--` and question mark `..--..`.  You may also wish to decode Morse in other languages. To do this you will need to edit the file `morse_lookup.py` and add the dictionary entries as appropriate.

A comprehensive reference for International Morse can be found [here](https://www.itu.int/rec/R-REC-M.1677-1-200910-I/en) which covers English, French, Arabic, Chinese and Russian.

There are also special procedural characters that conventionally mean things like wait, end of message or message part separator. These would certainly have been in use 100 years ago during 1914. Some of them are mentioned in the reference above but a more comprehensive discussion of Morse Code extensions can be found [here](http://ke1g.org/media/uploads/files/MorseExtension.pdf).

If you're serious about learning Morse then I would suggest that you have a read of [this discussion](http://www.qsl.net/n1irz/finley.morse.html) regarding the **Koch Method** of Morse training. This is a tried and tested way to learn Morse by listening at 15 to 20 words per minute. There is also an existing [Python package](https://pypi.python.org/pypi/KochMorse/0.99.7) which provides a Gtk2 style interface that you could install and use.

If you wish to use your `morse-code.py` project to *key in* at 15 to 20 words per minute you will need to modify some of the timing numbers that we hard coded. These are specifically in the `decoder_thread` function where we're testing `key_up_length >= 1.5` and `key_up_length >= 4.5` respectively. Those numbers would need to be reduced. I would recommend to reduce them in stages but ensure that the new word time (where we show a space) is always three times the length of the new letter time (where we decode the letter). Try 1 and 3 respectively and see how you fair before going lower.
