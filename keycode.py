#!/usr/bin/env python
# http://stackoverflow.com/questions/1918841/how-to-convert-ascii-character-to-cgkeycode */

import ctypes
import ctypes.util
import CoreFoundation
import Foundation
import objc

try:
    unichr
except NameError:
    unichr = chr

carbon_path = ctypes.util.find_library('Carbon')
carbon = ctypes.cdll.LoadLibrary(carbon_path)
    
# We could rely on the fact that kTISPropertyUnicodeKeyLayoutData has
# been the string @"TISPropertyUnicodeKeyLayoutData" since even the
# Classic Mac days. Or we could load it from the framework. 
# Unfortunately, the framework doesn't have PyObjC wrappers, and there's
# no easy way to force PyObjC to wrap a CF/ObjC object that it doesn't
# know about. So:
_objc = ctypes.PyDLL(objc._objc.__file__)
_objc.PyObjCObject_New.restype = ctypes.py_object
_objc.PyObjCObject_New.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
def objcify(ptr):
    return _objc.PyObjCObject_New(ptr, 0, 1)
kTISPropertyUnicodeKeyLayoutData_p = ctypes.c_void_p.in_dll(
    carbon, 'kTISPropertyUnicodeKeyLayoutData')
kTISPropertyUnicodeKeyLayoutData = objcify(kTISPropertyUnicodeKeyLayoutData_p)

carbon.TISCopyCurrentKeyboardInputSource.argtypes = []
carbon.TISCopyCurrentKeyboardInputSource.restype = ctypes.c_void_p
carbon.TISGetInputSourceProperty.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
carbon.TISGetInputSourceProperty.restype = ctypes.c_void_p
carbon.LMGetKbdType.argtypes = []
carbon.LMGetKbdType.restype = ctypes.c_uint32
OptionBits = ctypes.c_uint32
UniCharCount = ctypes.c_uint8
UniChar = ctypes.c_uint16
UniChar4 = UniChar * 4
carbon.UCKeyTranslate.argtypes = [ctypes.c_void_p, # keyLayoutPtr
                                  ctypes.c_uint16, # virtualKeyCode
                                  ctypes.c_uint16, # keyAction
                                  ctypes.c_uint32, # modifierKeyState
                                  ctypes.c_uint32, # keyboardType
                                  OptionBits,      # keyTranslateOptions
                                  ctypes.POINTER(ctypes.c_uint32), # deadKeyState
                                  UniCharCount,    # maxStringLength
                                  ctypes.POINTER(UniCharCount), # actualStringLength
                                  UniChar4]
carbon.UCKeyTranslate.restype = ctypes.c_uint32 # OSStatus
kUCKeyActionDisplay = 3
kUCKeyTranslateNoDeadKeysBit = 0

kTISPropertyUnicodeKeyLayoutData = ctypes.c_void_p.in_dll(
    carbon, 'kTISPropertyUnicodeKeyLayoutData')

def createStringForKey(keycode):
    keyboard_p = carbon.TISCopyCurrentKeyboardInputSource()
    keyboard = objcify(keyboard_p)
    layout_p = carbon.TISGetInputSourceProperty(keyboard_p, 
                                                kTISPropertyUnicodeKeyLayoutData)
    layout = objcify(layout_p)
    layoutbytes = layout.bytes()
    keysdown = ctypes.c_uint32()
    length = UniCharCount()
    chars = UniChar4()
    retval = carbon.UCKeyTranslate(layoutbytes.tobytes(),
                                   keycode,
                                   kUCKeyActionDisplay,
                                   0,
                                   carbon.LMGetKbdType(),
                                   kUCKeyTranslateNoDeadKeysBit,
                                   ctypes.byref(keysdown),
                                   4,
                                   ctypes.byref(length),
                                   chars)
    s = u''.join(unichr(chars[i]) for i in range(length.value))
    CoreFoundation.CFRelease(keyboard)
    return s

codedict = {createStringForKey(code): code for code in range(128)}
def keyCodeForChar(c):
    return codedict[c]

if __name__ == '__main__':
    import sys
    for arg in sys.argv[1:]:
        try:
            keycode = int(arg)
        except ValueError:
            print(u'{}: {}'.format(arg, keyCodeForChar(arg)))
        else:
            print('{}: {!r}'.format(keycode, createStringForKey(keycode)))
    if len(sys.argv) < 2:
        for keycode in range(128):
            print('{}: {!r}'.format(keycode, createStringForKey(keycode)))
