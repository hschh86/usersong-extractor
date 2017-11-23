"""
util.py

Utilities and helper functions that don't require mido

"""
import sys
# SysEx Manufacturer ID
YAMAHA = 0x43


# eprint
def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


# slicing and iteration
def slicebyn(obj, n, end=None):
    """
    Iterator over n-length slices of obj from the range 0 to end.
    end defaults to len(obj).
    """
    if end is None:
        end = len(obj)
    return (obj[i:i+n] for i in range(0, end, n))


def not_none_get(value, not_none):
    """Return value, or not_none if value is None"""
    if value is None:
        return not_none
    else:
        return value


# byte helpers
def assert_low(byte):
    """Raise ValueError if byte > 127"""
    if byte > 0x7F:
        raise ValueError("Byte value out of range: {}".format(byte))


# bitarray helpers
def boolean_bitarray_get(integer, index):
    """The index-th-lowest bit of the integer, as a boolean."""
    return bool((integer >> index) & 0x01)


def boolean_bitarray_tuple(integer, length=8):
    """
    Unpack an integer into a tuple of boolean values, LSB first.
    Uses the lowest bits up to length.
    Raises ValueError if any higher bits are set to 1
    """
    if integer >= (1 << length):
        raise ValueError("Some bits are too high: {}".format(integer))
    return tuple(boolean_bitarray_get(integer, i) for i in range(length))


# yamaha seven byte packing
def seven_byte_length(value):
    """
    Returns the minimum number of bytes required to represent the integer
    if we can use seven bits per byte.
    Positive integers only, please!
    """
    q, rem = divmod(value.bit_length(), 7)
    if rem or not q:
        # (the not q is in case value is 0, we can't have 0 bytes)
        q += 1
    return q


def pack_seven(value, length=None):
    """
    Packs a positive integer value into the seven-bit representation used
    in the sysex message data.
    """
    if value < 0:
        raise ValueError("Value is negative: {}".format(value))
    minlen = seven_byte_length(value)
    if length is None:
        length = minlen
    else:
        # if 2**(7*length) < value...
        if minlen > length:
            raise ValueError("Length too short to fit value")
    dest = bytearray(length)
    for i in range(minlen):
        dest[i] = (value & 0x7F)
        value >>= 7
    return bytes(reversed(dest))


# yamaha seven-byte unpacking & reconsitution
def unpack_seven(inbytes):
    """
    Reconstruct a number from the seven-bit representation used in
    the SysEx message data.
    Takes a bytes-like object, where each byte is seven bits of the number
    (big-endian byte order)
    Each byte must have its high bit zero, or else ValueError is raised.
    """
    value = 0
    for b in inbytes:
        assert_low(b)
        value = (value << 7) | b
    return value


def reconstitute(inbytes):
    """
    Unpack a sequence of eight bytes into a bytearray of seven bytes
    where the highest bit of each byte is determined by the eighth byte,
    that is, unpack eight bytes of the bulk dump payload data
    """
    if len(inbytes) != 8:
        raise ValueError("There must be eight bytes!")
    dest = bytearray(7)
    lastbyte = inbytes[7]
    assert_low(lastbyte)
    for i in range(7):
        byte = inbytes[i]
        assert_low(byte)
        highbit = (lastbyte << (i+1)) & 0x80
        dest[i] = byte | highbit
    return dest


def reconstitute_all(inbytes):
    """
    Unpack a sequence with a length a multiple of eight using the
    reconstitute function. Returns a bytes object.
    """
    if len(inbytes) % 8 != 0:
        raise ValueError("There must be a multiple of eight bytes!")
    # would a memoryview object instead of a slice would be better here?
    return b''.join(reconstitute(x) for x in slicebyn(inbytes, 8))


# midi number helper functions
def unpack_variable_length(inbytes, limit=True):
    """
    Reconstruct a number from the variable-length representation used
    in Standard MIDI files. This version only accepts just the entire sequence
    (that is, last byte must have high bit 0, all other bytes must have
    high bit 1).
    In actual MIDI files, the max length is four bytes. ValueError raised if
    length of inbytes exceeds four. (set limit=False to override this)
    """
    if limit and len(inbytes) > 4:
        raise ValueError("Sequence too long: {}".format(len(inbytes)))

    value = 0
    last = len(inbytes)-1
    for i, b in enumerate(inbytes):
        # check for validity
        if (b > 0x7F) is not (i < last):
            raise ValueError("Byte sequence not valid")
        value = (value << 7) | (b & 0x7F)
    return value


def pack_variable_length(value, limit=True):
    """
    Encode a positive integer as a variable-length number used in
    Standard MIDI files.
    ValueError rasied if value is over 0x0FFFFFFF (=would require >4 bytes).
    Set limit=False to override this.
    """
    if value < 0:
        raise ValueError("Value is negative: {}".format(value))
    if limit and value > 0x0FFFFFFF:
        raise ValueError("Value too large: {}".format(value))

    dest = bytearray()
    dest.append(value & 0x7F)
    value >>= 7
    while value:
        dest.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(dest))