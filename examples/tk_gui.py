# -*- coding: utf-8 -*-
# *****************************************************************************
#       Copyright (C) 2006-2020 Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#       Copyright (C) 2020 Bassem Girgis. <brgirgis@gmail.com>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************

""" Mockup of gui-use of pyreadline3


"""


import pyreadline3.logger as log
import Tkinter
from pyreadline3.keysyms.common import KeyPress
from pyreadline3.rlmain import BaseReadline

log.sock_silent = False


translate = {
    "plus": "+",
    "minus": "-",
    "asterisk": "*",
    "slash": "/",
    "exclam": "!",
    "quotedbl": '"',
    "parenleft": "(",
    "parenright": ")",
}


def KeyPress_from_event(event):
    keysym = event.keysym.lower()
    char = event.char
    if keysym in translate:
        keysym = translate[keysym]

    shift = event.state & 1 != 0
    control = event.state & 4 != 0
    meta = event.state & (131072) != 0

    if len(keysym) == 1 and control and meta:
        keysym = ""
    elif len(keysym) == 1:
        char = keysym
        keysym = ""

    return KeyPress(char, shift, control, meta, keysym)


class App:
    def __init__(self, master):
        self.frame = frame = Tkinter.Frame(master)
        frame.pack()
        self.lines = ["Hello"]
        self.RL = BaseReadline()
        self.RL.read_inputrc()
        self.prompt = ">>>"
        self.readline_setup(self.prompt)
        self.textvar = Tkinter.StringVar()
        self._update_line()
        self.text = Tkinter.Label(
            frame,
            textvariable=self.textvar,
            width=50,
            height=40,
            justify=Tkinter.LEFT,
            anchor=Tkinter.NW,
        )
        self.text.pack(side=Tkinter.LEFT)
        master.bind("<Key>", self.handler)
        self.locals = {}

    def handler(self, event):
        keyevent = KeyPress_from_event(event)
        try:
            result = self.RL.process_keyevent(keyevent)
        except EOFError:
            self.frame.quit()
            return
        if result:
            self.lines.append(self.prompt + " " + self.RL.get_line_buffer())
            line = self.RL.get_line_buffer()
            if line.strip():
                try:
                    result = eval(line, globals(), self.locals)
                    self.lines.append(repr(result))
                except BaseException:
                    self.lines.append("ERROR")
            self.readline_setup(self.prompt)
        self._update_line()

    def readline_setup(self, prompt=""):
        self.RL.readline_setup(prompt)

    def _update_line(self):
        self.textvar.set(
            "\n".join(self.lines + [self.prompt + " " + self.RL.get_line_buffer()])
        )


root = Tkinter.Tk()

display = App(root)
root.mainloop()
