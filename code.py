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
	except:
		pass

while True:
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
