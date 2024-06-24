import board
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import usb_hid
time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

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
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0",
    ".-.-.-": ".",
    "--..--": ",",
    "---...": ":",
    "..--..": "?",
    ".----.": "'",
    "-....-": "-",
    "-..-.": "/",
    "-.--.": "(",
    "-.--.-": ")",
    ".-..-.": "\"",
    "-...-": "=" }

def emitLetter(string):
    try:
        keyboard_layout.write(letters[string])
    except:
        pass

while True:
    # Start/stop timers depending on up or down
    # There will be no more than two transition points by defintion
    # Spaces determine which timer
    # When time comes to count a space, erase the previous reading
    # first before recording

    if (A1.value):  # Button is released
        if (prevstate ^ A1.value):  # Transition; reset and tally to dits
            print(silence)
            silence = 0
            if signal < (UNIT_TIME*2):  # Tally signal to ternary
                dits += "."
            else:
                dits += "-"
            #print(dits)
        else:  # Space => Record
            silence += 1
            if (silence < UNIT_TIME*2):
                pass
            elif (silence < (UNIT_TIME*6)):
                if dits != "":  # If anything is recorded, check against Letters, then reset it.
                    emitLetter(dits)  # <== See Below
                    dits = ""
            else:  # Timeout
                emitLetter(dits)  # func occurs both if typing resumes and if it stops.
                dits = ""
    else:  # Button is pressed
        if (prevstate ^ A1.value):  # Transition
            print(signal)
            signal = 0
        else:  # Space
            signal += 1
    #print(dits)
    prevstate = A1.value
    time.sleep(0.001)
