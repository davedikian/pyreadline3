"""
Example script using the callback interface of readline.

:author: strank
"""

__docformat__ = "restructuredtext en"

import msvcrt
import os
import readline
import time


prompting = True
count = 0
maxlines = 10


def main():
    readline.callback_handler_install(
        "Starting test, please do type:" + os.linesep, lineReceived
    )
    index = 0
    start = int(time.time())
    while prompting:
        # demonstrate that async stuff is possible:
        if start + index < time.time():
            readline.rl.console.title("NON-BLOCKING: %d" % index)
            index += 1
        # ugly busy waiting/polling on windows, using 'select' on Unix: (or use
        # twisted)
        if msvcrt.kbhit():
            readline.callback_read_char()
    print("Done, index =", index)


def lineReceived(line):
    global count, prompting
    count += 1
    print("Got line: %s" % line)
    if count > maxlines:
        prompting = False
        readline.callback_handler_remove()
    else:
        readline.callback_handler_install(
            "Got %s of %s, more typing please:" % (count, maxlines) + os.linesep,
            lineReceived,
        )


if __name__ == "__main__":
    main()
