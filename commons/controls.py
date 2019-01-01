"""
controls.py

For working with the controls / sysex / etc midi messages
"""

import mido

controls = {}
control_names = {}
for short, num, name in (
    ("bank_msb",           0x00, "Bank MSB"),
    ("bank_lsb",           0x32, "Bank LSB"),
    ("volume",             0x07, "Voice Volume"),
    ("pan",                0x0A, "Voice Pan"),
    ("reverb",             0x5B, "Voice Reverb Level"),
    ("chorus",             0x5D, "Voice Chorus Level"),
    ("pedal",              0x40, "Pedal Sustain"),
    ("release",            0x48, "Release Time"),
    ("modulation",         0x01, "Modulation Wheel"),
    ("expression",         0x0B, "Expression"),
    ("portamento_ctrl",    0x54, "Portamento Control"),
    ("harmonic",           0x47, "Harmonic Content"),
    ("attack",             0x49, "Attack Time"),
    ("brightness",         0x4A, "Brightness"),
    ("rpn_msb",            0x65, "RPN MSB"),
    ("rpn_lsb",            0x64, "RPN LSB"),
    ("data_msb",           0x06, "Data Entry MSB"),
    ("data_lsb",           0x26, "Data Entry LSB"),
    ("data_inc",           0x60, "Data Increment"),
    ("data_dec",           0x61, "Data Decrement"),
    ("sound_off",          0x78, "All Sound OFF"),
    ("sound_off_xmono",    0x7E, "All Sound OFF (MONO)"),
    ("sound_off_xpoly",    0x7F, "All Sound OFF (POLY)"),
    ("notes_off",          0x7B, "All Notes OFF"),
    ("notes_off_xomnioff", 0x7C, "All Notes OFF (OMNI OFF)"),
    ("notes_off_xomnion",  0x7D, "All Notes OFF (OMNI ON)"),
    ("reset_controls",     0x79, "Reset All Controls"),
    ("local",              0x7A, "Local ON/OFF"),
):
    controls[short] = num
    control_names[num] = name



def reverb(msb, lsb):
    return mido.Message(
        'sysex', data=(0x43, 0x10, 0x4c, 0x02, 0x01, 0x00, msb, lsb))


def chorus(msb, lsb):
    return mido.Message(
        'sysex', data=(0x43, 0x10, 0x4c, 0x02, 0x01, 0x20, msb, lsb))


def master_tuning(mm, ll):
    return mido.Message(
        'sysex', data=(0x43, 0x10, 0x27, 0x30, 0x00, 0x00, mm, ll, 0x00))


def master_tuning_val(value):
    if not (-100 <= value <= 100):
        raise ValueError("Value out of range: {}".format(value))
    mm, ll = divmod(value + 128, 16)
    return master_tuning(mm, ll)


def master_volume(mm):
    return mido.Message(
        'sysex', data=(0x7F, 0x7F, 0x04, 0x01, 0x00, mm))


def gm_system_on():
    return mido.Message(
        'sysex', data=(0x7E, 0x7F, 0x09, 0x01))


def local(boolean):
    if boolean:
        val = 0x7F
    else:
        val = 0x00
    return mido.Message('control_change', control=0x7A, value=val)


def set_rpn(msb=0x7F, lsb=0x7F, channel=0):
    return [
        mido.Message(
            'control_change', control=0x65, value=msb, channel=channel),
        mido.Message(
            'control_change', control=0x64, value=lsb, channel=channel)
    ]


def set_bank_program(msb, lsb, program, channel=0):
    return [
        mido.Message(
            'control_change', control=0x00, value=msb, channel=channel),
        mido.Message(
            'control_change', control=0x20, value=lsb, channel=channel),
        mido.Message(
            'program_change', program=program, channel=channel)
    ]


def multisend(port, messages):
    for message in messages:
        port.send(message)
