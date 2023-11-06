# *** Operation mirror top level nanovna-saver.py starts here:

import os.path
import sys

# Ignore the current working directory.
drc = os.path.join(os.path.dirname(__file__), "drc")

if os.path.exists(drc):
    sys.path.insert(0, drc)

# pylint: disable-next=wrong-import-position
import drc.NanoVNASaver.__main__


# The traditional test does not make sense here.
assert __name__ == "__main__"

drc.NanoVNASaver.__main__.main()






