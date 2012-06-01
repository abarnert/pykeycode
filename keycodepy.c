#include <Python.h>
#include "keycode.h"

static PyObject *cfStringConsumedToPy(CFStringRef s) {
  if (!s) Py_RETURN_NONE;
  CFIndex len = CFStringGetLength(s);
  UniChar *buffer = calloc(len+1, sizeof(UniChar));
  if (!buffer) {
    CFRelease(s);
    return NULL;
  }
  CFStringGetCharacters(s, CFRangeMake(0, len), buffer);
  CFRelease(s);
  return Py_BuildValue("u#", buffer, len);
}

static PyObject *
keycode_tostring(PyObject *self, PyObject *args) {
  int keyCode;
  if (!PyArg_ParseTuple(args, "i", &keyCode)) return NULL;
  return cfStringConsumedToPy(createStringForKey((CGKeyCode)keyCode));
}

static PyObject *
keycode_tokeycode(PyObject *self, PyObject *args) {
  char c;
  if (!PyArg_ParseTuple(args, "c", &c)) return NULL;
  return Py_BuildValue("i", keyCodeForChar(c));
}

static PyMethodDef KeycodeMethods[] = {
  {"tostring", keycode_tostring, METH_VARARGS,
   "Convert a keycode to the equivalent string"},
  {"tokeycode", keycode_tokeycode, METH_VARARGS,
   "Convert a character to the equivalent keycode"},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initkeycode(void) {
  (void)Py_InitModule("keycode", KeycodeMethods);
}
