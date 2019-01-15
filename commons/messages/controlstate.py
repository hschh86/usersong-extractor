"""
controlstate.py

Keeping track of the control messages!
"""

# We want to keep track of the state of the controls.
# purely as a visual aid.
# In theory, we feed in the messages to both an actual MIDI instrument
# and this module helpfully keeps track of what the
# instrument sees.

# We don't need to keep track of everything, just the interesting bits:
# the control changes, program changes, and some of the SysEx.
# No need for every single note!

# There are 16 channels. Humans read them as 1 to 16, but internally
# they're 0 to 15, or 0x0 to 0xF.

# Each channel has 128 controls that can be set,
# each with a value from 0 to 127.
# There are also the programs for each channel (0-127).
# Some settings are set with two different controls, one for MSB and LSB.
# Even further, there is the RPN settings, which are themselves set using
# multiple channel settings.
# The SysEx messages supported by the DGX-505 can also change state,
# for all channels. (so it appears at the instrument level.)
#  So there's a lot to keep track of.

# (Question: Does order matter? what happens when we change the LSB, then MSB?)

# (For more information consult the DGX505Midi.md document)

import re

from ..util import assert_low
from .controls import controls
from . import wrappers

# some control numbers
BANK_MSB = controls.num['bank_msb']
BANK_LSB = controls.num['bank_lsb']
RPN_MSB = controls.num['rpn_msb']
RPN_LSB = controls.num['rpn_lsb']
DATA_MSB = controls.num['data_msb']
DATA_LSB = controls.num['data_lsb']
DATA_INC = controls.num['data_inc']
DATA_DEC = controls.num['data_dec']
RESET_CONTROLS = controls.num['reset_controls']
LOCAL = controls.num['local']


class ChannelState(object):
    """
    A class that keeps track of the state of the controls of a channel.
    """
    def __init__(self, channel):
        """
        The channel parameter should be the channel number (0-15).
        """
        self._channel = channel

        # For simplicity, everything gets stored in dictionaries,
        # We have one for controls and two for the RPN data settings.
        self._controls = {}
        # The controls one should be keyed by the numbers
        self._data_msb = {}
        self._data_lsb = {}
        # and the rpn data ones by an (msb, lsb) tuple.

        # I don't know how the rpn and increment works so I just do them
        # independently with 2 separate dicts. Simple.

        # We also need to keep the state of the program:
        self._bank_program = (None, None, None)
        # Bank MSB, Bank LSB, Program, as bytes.
        # and that's basically it.

    def bank(self):
        return self._controls[BANK_MSB], self._controls[BANK_LSB]

    def rpn(self):
        return self._controls[RPN_MSB], self._controls[RPN_LSB]

    def bank_program(self):
        return self._bank_program

    def set_program(self, value):
        assert_low(value)

        # When the program is set, we save the current bank
        # and the program.

        self._bank_program = (*self.bank(), value)

    def set_control(self, control_num, value):
        # control_num and value should be integers 0-127
        assert_low(control_num)
        assert_low(value)

        self._controls[control_num] = value

        # Now we need to deal with rpn, for the data entry controls
        if control_num == DATA_MSB:
            self._data_msb[self.rpn()] = value
        elif control_num == DATA_LSB:
            self._data_lsb[self.rpn()] = value
        elif control_num == DATA_INC or control_num == DATA_DEC:
            rpn = self.rpn()
            msb = self._data_msb[rpn]
            if control_num == DATA_INC:
                if msb < 0x7F:
                    self._data_msb[rpn] = msb+1
            else:
                if msb > 0x00:
                    self._data_msb[rpn] = msb-1

    def get_rpn_data(self, msb, lsb):
        return self._data_msb[msb, lsb], self._data_lsb[msb, lsb]

    def data(self):
        return self.get_rpn_data(*self.rpn())

    def control_value(self, control_name):
        num = controls.num[control_name]
        return self._controls[num]


class MidiControlState(object):
    """
    A class that keeps track of the state of the MIDI controls.
    """

    def __init__(self):
        # There are 16 channels, we'll simply use a list to keep track of them
        self._channels = [ChannelState(n) for n in range(16)]

        # Additionally, we also have the sysex and a few other parameters
        # to keep track of.

        self._local = None
        self._master_vol = None
        self._master_tune = None
        self._reverb = None
        self._chorus = None


    def feed(self, msg):
        """
        Feed a mido message into the object, updating the internal state.
        """
        wrapped = wrappers.wrap(msg)

        if wrapped.type == 'program_change':
            # pass the program through
            self._channels[msg.channel].set_program(msg.program)
        elif wrapped.message.type == 'control_change':
            # is it a LOCAL?
            if wrapped.type == "local":
                self._local = wrapped.value
            # pass it through anyway
            self._channels[msg.channel].set_control(msg.control, msg.value)
        elif wrapped.type == "gm_on":
            # TODO: Find a way to reset to default values.
            # whatever they are.
            self.gm_reset()
        elif wrapped.type == "master_vol":
            self._master_vol = wrapped.value
        elif wrapped.type == "master_tune":
            self._master_tune = wrapped.value
        elif wrapped.type == "reverb":
            self._reverb = wrapped.msb, wrapped.lsb
        elif wrapped.type == "chorus":
            self._chorus = wrapped.msb, wrapped.lsb


    def gm_reset(self):
        # TODO: What are the default values?

        # "Automatically restores all default settings
        #  except Master Tuning" -- Manual

        # Reverb type is set to (01)Hall1
        # This would be 01 00
        self._reverb = 0x01, 0x00
        # Chorus type is set to (---)Chorus
        # I guess this would be 41 00
        self._chorus = 0x41, 0x00