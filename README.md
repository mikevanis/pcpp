# PCPP

Pre-Compile Pre-Processor (PCPP) is a Python script that helps with Python development between platforms. It imitates C-style `#define` and `#ifdef`. PCPP can watch a whole directory, or a specific Python file. 

## Why?
I develop a lot of Python scripts for the Raspberry Pi. They mostly utilise the PiCam, as well as various computer vision libraries. The differences between loading frames from a PiCam, and loading frames from a Mac's in-built webcam, are huge. You need to import different libraries, have different for loop structures, and you tend to forget these dependencies.

I come from the sane world of C, where you can use #defines to selectively precompile parts of code with precompiler conditionals. I really miss that in Python, so I recreated it with a watch script that acts as a precompiler. 

## How it works
PCPP isn't a fully-fledged precompiler yet. And by that I mean that it's pretty limited. You define the platform at the top, and PCPP will make a file that only has declarations and code related to that platform. You can't give defines values, and it is **not** a replacement utility. 

Here's an input example: 

	#define mac
	
	import cv2
	#ifdef pi
	import picam
	#endif
	
	#ifdef mac
	cv2.VideoCapture(0)
	#endif
	
	...
	
This is what the output will be after preprocessing:

	#define mac
	
	import cv2
	
	cv2.VideoCapture(0)
	
	...
	
You catch my drift? It's really useful for developing on the Pi, not very useful for much else!



## Installation
1. Clone this repo or download a zip.

2. Install watchdog with pip. 

		pip install watchdog
	
3. Copy `pcpp.py` into your project directory, or somewhere useful.

## Usage
Using PCPP is very simple. Just call it like this to track a directory. It will only track `*.py` files. 

	./pcpp.py -s path/to/files/
	
Call it like this to track the directory it's in:

	./pcpp.py -s .
	
And finally, call it like this to track a file:

	./pcpp.py -s path/to/file.py
	
## Further development
It would be really useful to turn this into a proper command line tool that you can install with homebrew. Unfortunately, this is good enough for now (at least for me). Regardless, if anyone else finds it useful, I'd love some help. 

Also, extending the functionality further to include pattern replacement, and other things that would bring it closer to a real preprocessor / precompiler, is cool. 

