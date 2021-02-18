#!/usr/bin/env python3

# uncomment to print debug info during instrumentation
# import assignhooks.transformer
# assignhooks.transformer.debug = True

import assignhooks.magic

# following import(s) will be instrumented
import testmod

print('======= WITH instrumentation ======')
testmod.fun()

# all imports are instrumented until this call is executed
assignhooks.magic.restore_import()

# following imoprt(s) will NOT be instrumented
# it is the same module actually, just with different name
# so that python attempts to import it (else it will ignore it)
import testmod2

print('======= WITHOUT instrumentation ======')
testmod2.fun()
