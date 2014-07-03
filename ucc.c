#include <CoreFoundation/CoreFoundation.h>
#include <ApplicationServices/ApplicationServices.h>

#define do(x) printf("%x\n", x);

int main() {
  do(NX_ALPHASHIFTMASK);
  do(NX_SHIFTMASK);
  do(NX_CONTROLMASK);
  do(NX_ALTERNATEMASK);
  do(NX_COMMANDMASK);
  do(NX_HELPMASK);
  do(NX_SECONDARYFNMASK);
  do(NX_NUMERICPADMASK);
  do(NX_NONCOALSESCEDMASK);
}
