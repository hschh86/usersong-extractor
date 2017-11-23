"""
slurp.py

writes out all midi messages, as bytes, to stdout, until enter pressed
"""
import sys
import argparse

import mido

from commons.util import eprint
from commons.mido_util import get_portname


argparser = argparse.ArgumentParser(
    description="Dumps midi messages as binary to stdout")
argparser.add_argument(
    'port', type=str,
    help="Port to read from (run 'mido-ports' to list available ports)")
argparser.add_argument(
    '-g', '--guessport', action='store_true',
    help="Guess which port to use (partial name match on PORT)")
argparser.add_argument(
    '-v', '--verbose', action='store_true',
    help="print human-readable messages to stderr")
args = argparser.parse_args()

inport_name = get_portname(args.port, args.guessport)


def msg_callback(message):
    # human readable to stderr
    if args.verbose:
        eprint(message)
    # bytes to stdout
    sys.stdout.buffer.write(message.bin())


with mido.open_input(inport_name, callback=msg_callback) as inport:
    eprint('Reading from port {!r}. Press enter to stop'.format(inport.name))
    # wait for any user input
    input()
    # just in case
    inport.callback = None