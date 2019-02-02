from fragment.cli import cli_main
from fragment.gui import gui_main
from fragment.strings import *
import sys
import getopt

interface = "cli" 

opts, args = getopt.getopt(sys.argv[1:], "i:", [])
for opt, arg in opts:
    if opt == "-i":
        interface = arg

if interface == "cli":
    cli_main()
elif interface == "gui":
    gui_main()
else:
    print(invalid_argument("-i"))
    sys.exit(1)
