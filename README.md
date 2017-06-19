**This is an archived resource.** The repo will remain available but the resource will no longer be maintained or updated. Some or all parts of the resource may no longer work. To see our latest resources, please visit [raspberrypi.org](http://www.raspberrypi.org).

# Morse Code Virtual Radio

How to program your Raspberry Pi to send, receive and decode Morse.

![](cover.png)

2014 marks the 100th anniversary of the declaration of [World War 1](http://en.wikipedia.org/wiki/World_War_I), which began on the 28th of July 1914. Over 16 million people lost their lives and 20 million were injured, making it one of the bloodiest conflicts in human history. It became known as the Great War and, subsequently, the First World War. To commemorate this event, we've come up with a way for you to simulate and experience the main form of radio communication that was used back then. Imagine being alive one hundred years ago, and sending and receiving messages that could mean life and death using only tones!

![](images/FWW_Centenary__Led_By_IWM_Red-web.png)

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

- 1 x [Morse Code key](http://www.nevadaradio.co.uk/amateur-radio/morse-keys/mfj-550)
- 2 (or more) x [Male-to-female jumper wires](http://shop.pimoroni.com/products/jumper-jerky)
- [Headphones or speakers](http://thepihut.com/products/mini-portable-speaker-for-the-raspberry-pi)

### Morse Code key options

A real Morse Code key will bring this project to life, especially if you can acquire an antique one. These can often be found in local antique shops all over the country. Alternatively you can also buy one online; see the links below.

- Buy new online (try [nevada radio](http://www.nevadaradio.co.uk/amateur-radio/morse-keys/mfj-550))

  ![](images/MFJ-550.png)

- Find an antique (try [eBay](http://search.ebay.co.uk/antique+morse+code+key))

  Make sure it works!

  ![](images/antique_key.png)

- Make your own!

  ![](images/homebrew_key.png)

## Worksheet & included files

- [The worksheet](worksheet.md)
- (Optional) Final version of Python code [final_code.py](code/final_code.py) and [morse_lookup.py](code/morse_lookup.py)
    - Download to your Pi with the following commands:

    ```bash
    wget https://goo.gl/K3Qlsa -O morse_lookup.py --no-check-certificate
    wget https://goo.gl/ilZqWF -O final_code.py --no-check-certificate
    sudo python final_code.py
    ```

## Licence

Unless otherwise specified, everything in this repository is covered by the following licence:

[![Creative Commons License](http://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

***Morse Code Virtual Radio*** by the [Raspberry Pi Foundation](https://www.raspberrypi.org/) is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

Based on a work at https://github.com/raspberrypilearning/morse-code-virtual-radio
