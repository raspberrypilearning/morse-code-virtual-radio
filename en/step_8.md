## Play a tone when the key is down

We've now proven that the value of the GPIO pin is changing when we press the Morse key, so the electronics is done. But our code is still very basic. All we have is a loop that keeps polling the pin; the code doesn't actually respond to the press or release of the key yet. You'll notice that you can press and release the key many times within one second.

For our Morse Code virtual radio to work, we need our program to respond every time the user presses or releases the key, by starting and stopping the tone sound. The `Button` class we created earlier already has a couple of methods to hold up the execution of your code until the key has been pressed or released. The overall goal here would be the following algorithm:

- Loop
  - Wait for key down
  - Start playing tone
  - Wait for key up
  - Stop playing tone

To wait for the press, we use two methods built into the `Button` class called `wait_for_press` and `wait_for_release`, which will make the Pi sleep until the pin state has changed. In order to have a good response time, we only need to sleep for a very short amount of time for each iteration of the loop: 0.01 seconds is ideal.

Have a look at the code below. Remember that this is for a pull up configuration; if you're using a pull down configuration, change the part that says `gpio.Button(pin, pull_up=True)` to `gpio.Button(pin, pull_up=False)`.

```python

tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 4
key = gpio.Button(pin, pull_up=True)

print("Ready")

while True:
    key.wait_for_press()
    tone_obj.play(-1) #the -1 means to loop the sound
    key.wait_for_release()
    tone_obj.stop()

```

Enter the following command to edit our previous program:

`nano morse-code.py`

Leave the `ToneSound` class at the top of your program, scroll to the bottom, delete the previous `while` loop code and then add the code above. Remember to make the necessary modifications if you are using a pull-down configuration.

Press `Ctrl + O` then `Enter` to save followed by `Ctrl + X` to quit.

You can now test your code.

```bash
./morse-code.py
```

After the you see the `Ready` message, you should be able to start keying in your first Morse Code messages. Test the Morse key to make sure that the tone is only ever on when the key is down, and off when the key is up. If you've got it the wrong way around, check again to see if you have the `pull_up` parameter set correctly.

Now have a go at a short word. Early Nokia mobile phones used the Morse Code for SMS when a text message arrived. This is a really easy one to do; the Morse Code for SMS is `... -- ...`. Try keying in other words using the chart at the top.

Press `Ctrl + C` to quit.

