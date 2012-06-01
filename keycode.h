#ifndef KEYCODE_H_INCLUDED_
#define KEYCODE_H_INCLUDED_
#include <CoreFoundation/CoreFoundation.h>
#include <ApplicationServices/ApplicationServices.h>
CFStringRef createStringForKey(CGKeyCode keyCode);
CGKeyCode keyCodeForChar(const char c);
#endif
