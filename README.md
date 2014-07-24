# Morse Code Virtual Radio

How to program your Raspberry Pi to send, receive and decode Morse.

![](./images/cover.png)

2014 marks the 100th anniversary of the declaration of [World War 1](http://en.wikipedia.org/wiki/World_War_I), which began on the 28th of July 1914. Over 16 million people lost their lives and 20 million were injured, making it one of the bloodiest conflicts in human history. It became known as the Great War and, subsequently, the First World War. To commemorate this event, we've come up with a way for you to simulate and experience the main form of radio communication that was used back then. Imagine being alive one hundred years ago, and sending and receiving messages that could mean life and death using only tones!

*Note: This resource uses International Morse.*

## Lesson objectives

- Understand what Morse Code is
- Understand how Morse was used for communication
- Understand how to send and receive Morse
- Understand a pull up circuit
- Understand a pull down circuit
- Understand multithreading

## Lesson outcomes

- To have programmed the Raspberry Pi to create Morse Code tones
- To have sent and decoded messages in Morse Code
- Gained experience in Python programming
- Gained experience using the Raspberry Pi GPIO pins
- Gained experience in multithreaded programming

## Requirements

### Hardware

- Raspberry Pi
- Micro USB power adaptor
- An SD Card with Raspbian already set up through NOOBS
- USB keyboard
- USB mouse
- HDMI cable
- Ethernet cable
- LAN with Internet connection
- A monitor or TV
- **Male** to **Female** jumper wires, at least 2 (try [Pimoroni](http://shop.pimoroni.com/products/jumper-jerky))

### Software

- python-pygame

### Extras: A Morse Code key

A real Morse Code key will bring this project to life, especially if you can acquire an antique one. These can often be found in local antique shops all over the country. Alternatively you can also buy one online; see the links below.

- Buy new online (try [nevada radio](http://www.nevadaradio.co.uk/amateur-radio/morse-keys/mfj-550))

  ![](./images/MFJ-550.png)

- Find an antique (try [eBay](http://search.ebay.co.uk/antique+morse+code+key))

  Make sure it works!

  ![](./images/antique_key.png)

- Make your own!

  ![](./images/homebrew_key.png)

### Time required

- 2 to 3 hours

## Steps

1. Setting up your Pi
1. Play a test beep
1. Connect the Morse Code key to the GPIO pins
1. Detect the key position through the GPIO pin value
1. Play a tone when the key is down
1. Decode the Morse as you go
1. Play a listening game with a friend

## Worksheet & included files

- [The worksheet](WORKSHEET.md)
- (Optional) Final version of Python code [final_code.py](./final_code.py)
    - Download to your Pi with the following commands:

    ```bash
    wget https://raw.githubusercontent.com/raspberrypilearning/morse-code/master/morse_lookup.py --no-check-certificate
    wget https://raw.githubusercontent.com/raspberrypilearning/morse-code/master/final_code.py --no-check-certificate
    chmod +x final_code.py
    sudo ./final_code.py
    ```

## Licence

Unless otherwise specified, everything in this repository is covered by the following licence:

![Creative Commons License](http://i.creativecommons.org/l/by-sa/4.0/88x31.png)

***Morse Code Virtual Radio*** by the [Raspberry Pi Foundation](http://raspberrypi.org) is licenced under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

Based on a work at https://github.com/raspberrypilearning/morse-code
