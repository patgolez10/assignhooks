#!/usr/bin/env python3

import assignhooks

# uncomment to print debug info during instrumentation
# assignhooks.instrument.debug = True
# assignhooks.patch.debug = True
# assignhooks.transformer.debug = True

assignhooks.instrument.start()    # following imports will be instrumentated
import testmod
assignhooks.instrument.stop()     # next imports won't be instrumented

print('======= WITH instrumentation ======')
testmod.fun()


# now importing wihout instrumentation
import testmod2

# it is the same module actually, just with different name
# so that python attempts to import it (else it will ignore it)
# and differnt assertions for expected results when not instrumented

print('======= WITHOUT instrumentation ======')
testmod2.fun()
