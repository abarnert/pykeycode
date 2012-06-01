#!/usr/bin/env python

import keycode
import sys

for arg in sys.argv[1:]:
    if arg and arg[0] == '-':
        print arg[1:], keycode.tostring(int(arg[1:]))
    else:
        for ch in arg:
            print ch, keycode.tokeycode(ch)
