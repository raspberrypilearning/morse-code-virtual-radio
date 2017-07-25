## Detect the key position through the GPIO pin value

Enter the following command to edit our previous tone program:

```bash
nano morse-code.py
```

To give us access to the GPIO pins in our code, we need to import the `gpiozero` library.

Add `gpiozero as gpio` to the `import` line at the top so that it reads:

```python
import pygame
import time
from RPi import GPIO
```

At the bottom remove these lines (they will be put back in again later):

```python
tone_obj.play(-1)
time.sleep(2)
tone_obj.stop()
```

Either copy and paste or enter the code below. Pay attention `key = gpio.Button(pin, pull_up=True)` line. This assigns the variable `key` to an *instance* of the class `gpio.Button`. The `gpio.Button` class holds all the important information about how to read inputs from the button, and comes with some *methods*, which are like functions, but are attached to the instance of the class, and can access its internal variables.

It also tells the class to set GPIO pin 4 as input, then set the internal pull up resistor on it. If you want to use the pull down resistor, you'll need to use `pull_up=False` instead.

Then, there is then a `while` loop, which continually reads the state of GPIO pin 4 and prints `ON` or `OFF` to the screen every second.

```python
pin = 4
key = gpio.Button(pin, pull_up=True)

while True:
    reading = key.is_pressed
    print("ON" if reading else "OFF")
    time.sleep(1)
```

Press `Ctrl + O` then `Enter` to save followed by `Ctrl + X` to quit.

If you've set the `pull_up` parameter to the right value, the program should show OFF when the key is up. Hold it down for a few seconds and it will show ON. The output should look something like this:

```bash
OFF
OFF
OFF
ON
ON
ON
OFF
OFF
OFF
```

If it is the other way round (it shows `ON` when the key is up and vice-versa), change the value of the `pull_up` parameter, then retry.

Press `Ctrl + C` to quit.

