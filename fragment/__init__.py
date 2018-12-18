from fragment import interface
import sys

if len(sys.argv) < 2:
    print("Please indicate whether to run Fragment in gui or cli mode.")
    exit(1)

mode = sys.argv[1]

if mode == "cli":
    interface.run_cli()
elif mode == "gui":
    interface.run_gui()
else:
    print("Invalid mode: {}".format(mode))
    exit(1)
