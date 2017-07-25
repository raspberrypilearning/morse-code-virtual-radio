## What next?

- Why not extend the decoding ability of this project to include punctuation characters like the full stop `.-.-.-`, comma `--..--` and question mark `..--..`?  
- You could try to decode Morse in other languages. To do this you will need to edit the file `morse_lookup.py` and add the dictionary entries as appropriate. A comprehensive reference for International Morse can be found [here](https://www.itu.int/rec/R-REC-M.1677-1-200910-I/en), covering English, French, Arabic, Chinese and Russian.
- You could explore Morse Code extensions: these are special procedural characters that mean things like wait, end of message or message part separator. You can find more information on these extensions [here](http://ke1g.org/media/uploads/files/MorseExtension.pdf).
- You could take your Morse Code knowledge further with the [Koch Method](http://www.qsl.net/n1irz/finley.morse.html), a tried and tested way to learn Morse by listening at 15 to 20 words per minute. There is also an existing [Python package](https://pypi.python.org/pypi/KochMorse/0.99.7) which provides a Gtk2 style interface that you could install and use.
- Can you work out how to modify the timing numbers we hard coded to enable you to use your `morse-code.py` project to key in at 15 to 20 words per minute? Try changing the `key_up_length` in the `decoder_thread` function. 

