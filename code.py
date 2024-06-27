import board
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import usb_hid
time.sleep(1)
keyboard = Keyboard(usb_hid.devices)

import digitalio
A1 = digitalio.DigitalInOut(board.A1)  # Input object
A1.direction = digitalio.Direction.INPUT
A1.pull = digitalio.Pull.UP
prevstate = A1.value

import time

dits = ""
signal = 0
silence = 0

UNIT_TIME = 120  # Time in mill's for a 'dit'
letters = {
	# Letters
	".-": Keycode.A,
	"-...": Keycode.B,
	"-.-.": Keycode.C,
	"-..": Keycode.D,
	".": Keycode.E,
	"..-.": Keycode.F,
	"--.": Keycode.G,
	"....": Keycode.H,
	"..": Keycode.I,
	".---": Keycode.J,
	"-.-": Keycode.K,
	".-..": Keycode.L,
	"--": Keycode.M,
	"-.": Keycode.N,
	"---": Keycode.O,
	".--.": Keycode.P,
	"--.-": Keycode.Q,
	".-.": Keycode.R,
	"...": Keycode.S,
	"-": Keycode.T,
	"..-": Keycode.U,
	"...-": Keycode.V,
	".--": Keycode.W,
	"-..-": Keycode.X,
	"-.--": Keycode.Y,
	"--..": Keycode.Z,
	# Numbers
	".----": Keycode.ONE,
	"..---": Keycode.TWO,
	"...--": Keycode.THREE,
	"....-": Keycode.FOUR,
	".....": Keycode.FIVE,
	"-....": Keycode.SIX,
	"--...": Keycode.SEVEN,
	"---..": Keycode.EIGHT,
	"----.": Keycode.NINE,
	"-----": Keycode.ZERO,
	# Math
	"-...-": Keycode.EQUALS,
	"-.--.": Keycode.KEYPAD_PLUS,
	"-.---": Keycode.MINUS, #-_
	".-.--": Keycode.KEYPAD_ASTERISK,
	".-..-": Keycode.FORWARD_SLASH,  # /&?
	"--.--": Keycode.BACKSLASH,  # & |
	".--..": 116,  # (
	".--.-": 117,  # )
	"--.-.": 118,  # {
	"--..-": 119,  # }
	"-..-.": "[",
	"-..--": "]",
	# Punctuation
	".-.-.-": Keycode.PERIOD,
	"--..--": Keycode.COMMA,  # ,<
	"---...": "Keycode.COLON",
	"..-.-": Keycode.SEMICOLON,  #;:
	"..--..": "?",
	"..--.": "!",
	".-..-.": Keycode.QUOTE,
	".----.": "'",  # May be tied to quote
	"---.-": Keycode.POUND,  # #&~
	
	# Arrows
	"..-..": Keycode.UP_ARROW,
	".-.-.": Keycode.DOWN_ARROW,
	".-...": Keycode.LEFT_ARROW,
	"...-.": Keycode.RIGHT_ARROW,
	# Functions
	".-.-": Keycode.ESCAPE,
	"---.": Keycode.SPACE,
	"----": Keycode.BACKSPACE,  # BACK
	".---.": Keycode.ENTER,
	"....--": Keycode.DELETE,
	".----.": 43,  # TAB
	# Toggles
	"..--": Keycode.SHIFT,
	"-.-..": Keycode.CONTROL,
	"-.-.-": Keycode.ALT,
	# Unused
	"-.....": 124,  # COPY
	".-....": 123,  # CUT
	"..-...": 125,  # PASTE
	"...-..": 122,  # UNDO
	".....-": "SAVE",  # SAVE
	"..--..": "?",
	"..--.": "!",
	"---...": "Keycode.COLON",
	}

toglist = {"..--": 0, "-.-..": 0, "-.-.-": 0,}  # Specific keys to be toggled

def emitLetter(code):
    try:
        keyboard.press(letters[code])
        time.sleep(0.001)
        try: 
            toglist[code]  # Check wanted list
        except:
            keyboard.release(letters[code])
            print("normal character")
        else:  # Match Found
            if toglist[code]:
                keyboard.release(letters[code])
                print("released")
            toglist[code] ^= 1

while True:
    # Start/stop timers depending on up or down
    # There will be no more than two transition points by defintion
    # Spaces determine which timer
    # When time comes to count a space, erase the previous reading
    # first before recording

    if (A1.value):  # Button is released
        if (prevstate ^ A1.value):  # Transition; reset and tally to dits
            if signal < (UNIT_TIME*2):  # Tally signal to ternary
                dits += "."
            else:
                dits += "-"
            silence = 0
        else:  # Space => Record
            silence += 1
            if (silence < UNIT_TIME*2):
                pass
            elif (silence < (UNIT_TIME*6)):
                if dits != "":  # Check dictionary
                    emitLetter(dits)  # <== See Below
                    dits = ""
            else:  # Timeout
                emitLetter(dits)  # func occurs both if typing resumes and if it stops.
                dits = ""
    else:  # Button is pressed
        if (prevstate ^ A1.value):  # Transition
            signal = 0
        else:  # Space
            signal += 1
    prevstate = A1.value
    time.sleep(0.001)
