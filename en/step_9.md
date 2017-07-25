## Decode the Morse as you go

What will really help you learn is having a way to know when you're getting the code right or wrong. We can program the Pi to decode what you're keying in and then print the letters to the screen as you go. With this you can pick a message, try to key it in and immediately see if the correct text is being displayed. If the wrong text comes up then it's likely that you didn't key in the correct Morse Code sequence. Practice makes perfect!

To program this, we should remind ourselves about the rules of International Morse Code:

- All timings are defined as multiples of one dot length
- A dash is three times the length of a dot
- Each dot or dash has a short gap of silence after it (usually 1 dot length)
- Letters in a word have a slightly longer gap of silence between them (usually 3 dot lengths)
- Words have an even longer gap of silence between them (usually 7 dot lengths)

So to start with, we need to tell the difference between a dot and a dash. We can do that by timing how long the key is held down for to give us the length of the tone. Then we need to tell the difference between the dots and dashes making up one word and the next. To do that, we can time how long the key is up for, so we're measuring the gap of silence between the tones. The same measurement of time will also give us the difference between letters making up a word and separate words.

### Distinguish dot and dash

First, we need to program the Pi to recognise the difference between a dot and a dash.

The aim is to time how long the key is held down for. Generally speaking, a dot is about 0.15 seconds or less and anything longer than this is a dash. You're welcome to use a different value if you wish but 0.15 seconds is a good starting point. The way to time something in code is to record the time now, wait until something has happened, and then subtract the time you recorded from the current time.

Take a look at the code below; notice the the use of the `key_down_time` and `key_down_length` variables.

```python

tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 4
key = gpio.Button(pin, pull_up=True)

DOT = "."
DASH = "-"

key_down_time = 0
key_down_length = 0

print("Ready")

while True:
    key.wait_for_press()
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    key.wait_for_release()
    key_down_length = key_up_time - key_down_time #get the length of time it was held down for
    tone_obj.stop()

    if key_down_length > 0.15:
        print(DASH)
    else:
        print(DOT)
```

Enter the following command to edit our previous program:

```bash
nano morse-code.py
```

Scroll to the bottom and add the lines shown above that are missing from your original code. If necessary, modify the code for a pull down configuration. When you're done press `Ctrl + O` then `Enter` to save followed by `Ctrl + X` to quit. You can now test your code.

```bash
./morse-code.py
```

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

Press `Ctrl + C` to quit.

### Translate Morse Code into text

Next, we need a way to combine these dots and dashes to form letters and words. This is actually a little more tricky than it sounds. Consider how we're going to know when the user has finished keying in a letter and when they have finished a word. The correct behaviour will be the following:

- When they finish keying in a letter, display the letter
- When they finish keying in a word, display a space character

The following code should make this easier, by allowing you to take a string of dots and dashes and look up the corresponding letter of the alphabet. Enter the following command to download this code:

```bash
wget https://goo.gl/aRjulj -O morse_lookup.py --no-check-certificate
```

Now let's have a look at it. Enter the command below to edit the file:

```bash
nano morse_lookup.py
```

The `morse_code_lookup` variable is a Python dictionary object. A dictionary works using keys and values; for every key there is a corresponding value. You could create a dictionary to translate between, say, English and French. In this case, if the key was "Hello", the value would be "Bonjour". Look at the code below as an example:

```python
english_to_french = {
    "Hello": "Bonjour",
    "Yes": "Oui",
    "No": "Non"
}
    
print(english_to_french["Hello"])
```

The result of the above code would be: `Bonjour`.

We're going to use this technique to translate between the sequence of dots and dashes and their corresponding letter. For example, `-.-.` is the letter `C`. The `try_decode` function at the bottom can be used to check that a dot-dash sequence is valid and, if so, translate it into the corresponding letter.

Press `Ctrl + X` to quit from editing without saving.

### Multithreading 

Here, we need to introduce a new programming concept called [multithreading](http://en.wikipedia.org/wiki/Multithreading_%28software%29#Multithreading). A thread in a program is a single sequence of instructions that are being followed by the computer at any one time. In most simple programs there is only one thread, which is the main one. But it is possible to have multiple threads going at the same time: this is like making a program pat its head and rub its stomach at the same time.

Because our main thread is always held up by the `wait_for_keydown` and `wait_for_keyup` functions, we need to have another thread which can constantly do the work of decoding what the user is keying in.

The overall goal here will be to modify the main thread so that it stores every dot and dash in a buffer list. The decoder thread will then be watching independently for different lengths of silence. A short gap of silence denotes a new letter, so the thread will use the `try_decode` function to see if the buffer contents matches a letter; it will also empty the buffer. If the gap of silence gets longer, this denotes a new word and a space character would be shown.

### Add the code

Now let's go back to editing our main program. Enter the following command:

```bash
nano morse-code.py
```

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

print("Ready")

while True:
    key.wait_for_press()
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    key.wait_for_release()
    key_up_time = time.time() #record the time when the key was released
    key_down_length = key_up_time - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    buffer.append(DASH if key_down_length > 0.15 else DOT)
```

Double-check that your code is the same as the above. When you're done, press `Ctrl + O` then `Enter` to save. We're not finished editing, yet, though; do not run the code as it is. We still need to add code for the new thread.

First we need to add some new imports to the top of our file. Scroll up to the top and find the `import` lines. We need to add `_thread` to do multithreading and `from morse_lookup import *` to give us access to the lookup code we downloaded earlier. The code should now look like this:

```python
#!/usr/bin/python3
import pygame
import time
import gpiozero as gpio
import _thread as thread
from array import array
from pygame.locals import *
from morse_lookup import *
```

Next, let's put in the code that will run on our separate thread. To do this, you can just define a function and this will be what is run on that thread. Add this function to your code just below the `wait_for_keyup` function:

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

The first thing you'll notice is the use of the `global` keyword. This will give the thread access to the `key_up_time` and `buffer` variables that belong to the main thread, so that they can be used here. Next, we have a variable called `new_word`. Once the end of the word has been detected we set this to `False`, so that we don't keep putting more spaces down.

We then have another `while True` loop; the main purpose of this is to continually monitor the gaps of silence between tones. You'll see there is a `sleep` command to avoid overloading the CPU; then we calculate the `key_up_length`, which is the `key_up_time` from the main thread subtracted from the current time. Every time around the loop, which is every 0.01 seconds, the `key_up_length` value will increase as long as the Morse key stays up.

Next is an `if` statement. There are two conditions upon which we need to act here:

- When there is something in the `buffer` and the gap of silence is big enough to mean a new letter. We're hard-coding the value of `1.5` seconds for this. If this situation happens we know we're in a new word, so we set the `new_word` variable to `True`. The line `bit_string = "".join(buffer)` is taking the dots and dashes in the `buffer` list, and turning them into a single string that might be something like `.-..`. We can then see if that matches a key in the Morse translation dictionary via the `try_decode` function. The `try_decode` function displays the result. We then empty the buffer, ready for the next word, with `del buffer[:]`. If we didn't do this, the buffer would keep getting bigger, and would never match any letters in the `morse_lookup.py` dictionary.

- When the gap of silence has increased to `4.5` seconds. Remember that a rule of Morse is that the gap of silence for a new word has to be three times the length of the gap that denotes a new letter: `1.5 x 3 = 4.5`. So here we set `new_word` to False, so that the `else if` condition no longer succeeds, and then put down a space character.

Note that the use of `sys.stdout` is so that we can print to the screen without having to always show a new line, as with the default `print` command.

The choice of `1.5` and `4.5` seconds is essentially arbitrary, but these gaps are about right for someone who is new to Morse, who will be going quite slowly. As your skill improves, you may wish to reduce these numbers in your code. 

Press `Ctrl + O` then `Enter` to save. There is one more thing we need to do before we can run our code, which is to add a line of code that will launch the new thread. This has to be done from the main thread, so scroll down and find the `print("Ready")` line. Add the line below just before it:

```bash
thread.start_new_thread(decoder_thread, ())
```

The final code should look like the example below; remember to make the necessary changes if you're using a pull down configuration instead of pull up. 

```python
#!/usr/bin/python3
import pygame
import time
import gpiozero as gpio
import _thread as thread
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
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

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

pin = 4
key = gpio.Button(pin, pull_up=True)

DOT = "."
DASH = "-"

key_down_time = 0
key_down_length = 0
key_up_time = 0
buffer = []

thread.start_new_thread(decoder_thread, ())

print("Ready")

while True:
    key.wait_for_press()
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    key.wait_for_release()
    key_up_time = time.time() #record the time when the key was released
    key_down_length = key_up_time - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    buffer.append(DASH if key_down_length > 0.15 else DOT)
```

When you're done, press `Ctrl + O` then `Enter` to save, followed by `Ctrl + X` to quit. You can now test your code. 

```bash
./morse-code.py
```

Wait for the `Ready` message to show and then begin keying Morse Code in. The trick is to watch the screen and wait for a letter to appear before you start keying in the next one. You may wish to refer to the charts at the top of this page.

SOS is `...` `---` `...`

Hello is `....` `.` `.-..` `.-..` `---`

The output should look like this:

```
SOS HELLO 
```

Press `Ctrl + C` twice to quit.

You can ignore the message saying `Unhandled exception in thread`; this is just the child thread being terminated when you send the `KeyboardInterrupt` with `Ctrl + C`.

