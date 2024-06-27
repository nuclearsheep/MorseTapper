# MorseTapper
CircuitPython morse "keyboard" originally ported from an arduino project by Jacek Fedoryński. Intended for use on a SAMD21e18 QT py board. 
This code is useful to get around hardware limits, i.e the QT PY having limited pins, while being able to fully use a computer terminal.

    # Start/stop timers depending on up or down
    # There will be no more than one transition point per key press 
    # and per release
    # Value of the signal (1 or 0) determines which timer counts
    # When time comes to count a space, erase the previous reading
    # first before recording
    # A value is typed at both the end of a word where typing resumes
    # or timeout
    #
