import pytest
import io

import extractor as e

testdata = [("""
F0 43 73 7F 44 06 09 06 30 06 2E 00 00 00 50 53 52 03 01 00 00 00 39 39 05 64
00 3B 00 00 60 40 28 00 00 00 2D 00 00 64 40 08 00 7F 00 00 22 7F 50 40 2A 00
02 20 02 01 00 01 50 7F 0C 02 3C 00 00 40 00 00 01 00 07 00 36 36 05 64 01 40
67 00 68 40 1C 00 00 00 00 35 01 72 40 08 00 00 00 00 35 00 46 40 20 00 00 02
01 07 00 01 64 00 7F 0C 76 00 00 40 00 40 00 01 3D 00 36 36 05 00 64 00 54 7F
6E 40 22 08 00 7F 00 36 00 7F 40 00 08 00 7F 00 35 7F 5A 02 40 20 00 02 01 01
00 00 02 50 7F 0C 76 00 00 10 40 00 00 01 00 00 36 00 36 05 64 00 59 00 50 00
40 28 00 00 00 2D 00 00 64 40 08 00 7F 01 7A 00 00 47 40 24 00 02 02 00 01 00
02 5A 7F 0C 3C 04 00 00 40 00 00 01 7F 01 7F 39 39 7F 7F 00 34 4C 00 7F 40 28
00 00 00 00 2D 00 64 40 08 00 7F 00 00 35 7F 3F 40 28 00 10 02 02 01 00 01 5A
7F 01 0C 7F 00 00 40 00 00 20 01 00 00 39 39 05 64 00 00 53 00 68 40 1C 00 20
00 00 2D 00 64 40 08 00 00 7F 01 30 00 46 40 08 20 00 02 02 01 00 01 00 64 7F
0C 3C 00 00 40 20 00 00 01 07 00 36 36 08 05 64 00 41 7F 5E 40 04 2E 00 7F 00
35 01 72 00 40 08 00 00 00 43 00 00 46 40 32 00 02 01 07 00 00 02 50 7F 0C 76
00 08 00 40 00 00 01 07 01 02 39 39 05 64 00 34 00 00 7F 40 28 00 7F 00 34 00
00 64 40 08 00 7F 00 00 35 7F 3F 40 28 00 02 20 01 07 7F 02 5A 7F 0C 02 76 00
00 40 00 00 01 00 7F 7F 36 36 7F 7F 00 66 00 00 6E 40 14 00 00 00 00 2D 00 64
40 08 00 00 7F 00 04 7F 63 40 32 08 00 02 01 01 00 02 50 00 7F 0C 7F 00 00 40
00 50 00 01 00 00 36 36 05 00 64 01 4F 00 68 40 1C 00 00 00 00 2D 00 64 40 00
08 00 00 00 35 00 46 00 40 20 00 02 02 01 00 00 01 64 7F 0C 3C 00 00 10 40 00
00 01 0F 00 37 00 37 05 64 00 6D 00 70 00 40 28 22 00 00 06 00 00 64 40 08 00
7F 00 34 00 00 46 40 24 00 02 03 00 01 00 01 50 7F 0C 44 04 00 00 40 00 00 01
00 00 00 36 36 05 64 00 35 00 00 56 40 28 00 00 00 00 2D 00 64 40 08 00 7F 00
00 34 7F 59 40 28 1E 10 02 02 01 00 01 5A 7F 01 0C 3C 00 00 40 00 00 00 01 00
00 39 39 05 64 00 01 6F 7F 7F 40 1C 00 10 7F 00 35 00 64 40 08 00 00 7F 00 34
00 5F 40 00 20 00 02 02 01 00 01 00 64 7F 0C 3C 00 00 40 20 00 00 01 00 00 39
39 00 05 64 00 21 00 68 40 08 1C 00 00 00 2D 00 64 00 40 08 00 7F 00 66 00 00
46 40 20 00 02 02 01 00 00 01 64 7F 0C 3C 00 08 00 40 00 00 01 00 00 00 39 39
05 64 00 41 00 00 5E 40 2E 00 7F 00 1B 00 00 2F 40 08 00 7F 00 00 43 7F 46 40
32 00 02 20 02 01 00 02 50 7F 0C 02 3C 00 00 40 00 00 01 00 00 00 36 36 05 64
00 00 35 00 56 40 28 00 00 00 00 2D 00 64 40 08 00 00 7F 00 57 00 59 40 28 00
1E 02 02 01 00 01 5A 00 7F 0C 3C 00 00 40 00 40 00 50 53 52 03 00 00 00 30 F7
F0 43 73 7F 44 06 09 00 01 00 01 7F 7F 7F F7
""".encode('ascii'),  {
    'Style number': 1,
    'Accompaniment': 'OFF',
    'Split Point': 54,
    'Main A/B': 'Main B',
    'Style Volume': 100,
    'Tempo': 92,
    'Main Voice number': 54,
    'M. Volume': 86,
    'M. Octave': 0,
    'M. Pan': 64,
    'M. Reverb Level': 40,
    'M. Chorus Level': 0,
    'Dual Voice number': 53,
    'Dual': 'ON',
    'D. Volume': 89,
    'D. Octave': -1,
    'D. Pan': 64,
    'D. Reverb Level': 40,
    'D. Chorus Level': 30,
    'Split Voice number': 46,
    'Split': 'OFF',
    'S. Volume': 100,
    'S. Octave': 0,
    'S. Pan': 64,
    'S. Reverb Level': 8,
    'S. Chorus Level': 0,
    'Reverb Type': '02 Hall2',
    'Chorus Type': '01 Chorus1',
    'Sustain': 'OFF',
    'Harmony': 'OFF',
    'Harmony Type': '01 Duet',
    'Harmony Volume': 90,
    'Transpose': 0,
    'Pitch Bend Range': 2
}), ("""
F0 43 73 7F 44 06 09 06 30 06 2E 00 00 00 50 53 52 03 01 00 00 00 39 39 05 64
00 3B 00 00 60 40 28 00 00 00 2D 00 00 64 40 08 00 7F 00 00 22 7F 50 40 2A 00
02 20 02 01 00 01 50 7F 0C 02 3C 00 00 40 00 00 01 00 07 00 36 36 05 64 01 40
67 00 68 40 1C 00 00 00 00 35 01 72 40 08 00 00 00 00 35 00 46 40 20 00 00 02
01 07 00 01 64 00 7F 0C 76 00 00 40 00 40 00 01 3D 00 36 36 05 00 64 00 54 7F
6E 40 22 08 00 7F 00 36 00 7F 40 00 08 00 7F 00 35 7F 5A 02 40 20 00 02 01 01
00 00 02 50 7F 0C 76 00 00 10 40 00 00 01 00 00 36 00 36 05 64 00 59 00 50 00
40 28 00 00 00 2D 00 00 64 40 08 00 7F 01 7A 00 00 47 40 24 00 02 02 00 01 00
02 5A 7F 0C 3C 04 00 00 40 00 00 01 7F 01 7F 39 39 7F 7F 00 34 4C 00 7F 40 28
00 00 00 00 2D 00 64 40 08 00 7F 00 00 35 7F 3F 40 28 00 10 02 02 01 00 01 5A
7F 01 0C 7F 00 00 40 00 00 20 01 00 00 39 39 05 64 00 00 53 00 68 40 1C 00 20
00 00 2D 00 64 40 08 00 00 7F 01 30 00 46 40 08 20 00 02 02 01 00 01 00 64 7F
0C 3C 00 00 40 20 00 00 01 07 00 36 36 08 05 64 00 41 7F 5E 40 04 2E 00 7F 00
35 01 72 00 40 08 00 00 00 43 00 00 46 40 32 00 02 01 07 00 00 02 50 7F 0C 76
00 08 00 40 00 00 01 07 01 02 39 39 05 64 00 34 00 00 7F 40 28 00 7F 00 34 00
00 64 40 08 00 7F 00 00 35 7F 3F 40 28 00 02 20 01 07 7F 02 5A 7F 0C 02 76 00
00 40 00 00 01 00 7F 7F 36 36 7F 7F 00 66 00 00 6E 40 14 00 00 00 00 2D 00 64
40 08 00 00 7F 00 04 7F 63 40 32 08 00 02 01 01 00 02 50 00 7F 0C 7F 00 00 40
00 50 00 01 00 00 36 36 05 00 64 01 4F 00 68 40 1C 00 00 00 00 2D 00 64 40 00
08 00 00 00 35 00 46 00 40 20 00 02 02 01 00 00 01 64 7F 0C 3C 00 00 10 40 00
00 01 0F 00 37 00 37 05 64 00 6D 00 70 00 40 28 22 00 00 06 00 00 64 40 08 00
7F 00 34 00 00 46 40 24 00 02 03 00 01 00 01 50 7F 0C 44 04 00 00 40 00 00 01
36 00 01 2F 2F 00 2A 00 42 01 02 6F 23 25 01 7F 00 00 09 7F 70 37 29 03 00 20
00 2D 01 71 2D 26 02 00 07 09 05 7F 1A 64 7F 01 09 5A 00 00 6E 00 00 00 01 00
00 39 39 05 64 00 01 6F 7F 7F 40 1C 00 10 7F 00 35 00 64 40 08 00 00 7F 00 34
00 5F 40 00 20 00 02 02 01 00 01 00 64 7F 0C 3C 00 00 40 20 00 00 01 00 00 39
39 00 05 64 00 21 00 68 40 08 1C 00 00 00 2D 00 64 00 40 08 00 7F 00 66 00 00
46 40 20 00 02 02 01 00 00 01 64 7F 0C 3C 00 08 00 40 00 00 01 00 00 00 39 39
05 64 00 41 00 00 5E 40 2E 00 7F 00 1B 00 00 2F 40 08 00 7F 00 00 43 7F 46 40
32 00 02 20 02 01 00 02 50 7F 0C 02 3C 00 00 40 00 00 01 00 00 00 36 36 05 64
00 00 35 00 56 40 28 00 00 00 00 2D 00 64 40 08 00 00 7F 00 57 00 59 40 28 00
1E 02 02 01 00 01 5A 00 7F 0C 3C 00 00 40 00 40 00 50 53 52 03 00 00 00 4D F7
F0 43 73 7F 44 06 09 00 01 00 01 7F 7F 7F F7
""".encode('ascii'), {
    'Style number': 55,
    'Accompaniment': 'ON',
    'Split Point': 47,
    'Main A/B': 'Main A',
    'Style Volume': 42,
    'Tempo': 122,
    'Main Voice number': 195,
    'M. Volume': 111,
    'M. Octave': +2,
    'M. Pan': 35,
    'M. Reverb Level': 37,
    'M. Chorus Level': 1,
    'Dual Voice number': 46,
    'Dual': 'OFF',
    'D. Volume': 113,
    'D. Octave': 1,
    'D. Pan': 45,
    'D. Reverb Level': 38,
    'D. Chorus Level': 2,
    'Split Voice number': 10,
    'Split': 'ON',
    'S. Volume': 112,
    'S. Octave': -1,
    'S. Pan': 55,
    'S. Reverb Level': 41,
    'S. Chorus Level': 3,
    'Reverb Type': '09 Plate2',
    'Chorus Type': '05 Off',
    'Sustain': 'ON',
    'Harmony': 'ON',
    'Harmony Type': '26 Echo 1/32 note',
    'Harmony Volume': 100,
    'Transpose': -3,
    'Pitch Bend Range': 7
}), (b'\xf0Cs\x7fD\x06\t\x060\x06.\x00\x00\x00PSR\x03\x01\x00\x00\x0099\x05d\x00;\x00\x00`@(\x00\x00\x00-\x00\x00d@\x08\x00\x7f\x00\x00"\x7fP@*\x00\x02 \x02\x01\x00\x01P\x7f\x0c\x02<\x00\x00@\x00\x00\x01\x00\x07\x0066\x05d\x01@g\x00h@\x1c\x00\x00\x00\x005\x01r@\x08\x00\x00\x00\x005\x00F@ \x00\x00\x02\x01\x07\x00\x01d\x00\x7f\x0cv\x00\x00@\x00@\x00\x01=\x0066\x05\x00d\x00T\x7fn@"\x08\x00\x7f\x006\x00\x7f@\x00\x08\x00\x7f\x005\x7fZ\x02@ \x00\x02\x01\x01\x00\x00\x02P\x7f\x0cv\x00\x00\x10@\x00\x00\x01\x00\x006\x006\x05d\x00Y\x00P\x00@(\x00\x00\x00-\x00\x00d@\x08\x00\x7f\x01z\x00\x00G@$\x00\x02\x02\x00\x01\x00\x02Z\x7f\x0c<\x04\x00\x00@\x00\x00\x01\x7f\x01\x7f99\x7f\x7f\x004L\x00\x7f@(\x00\x00\x00\x00-\x00d@\x08\x00\x7f\x00\x005\x7f?@(\x00\x10\x02\x02\x01\x00\x01Z\x7f\x01\x0c\x7f\x00\x00@\x00\x00 \x01\x00\x0099\x05d\x00\x00S\x00h@\x1c\x00 \x00\x00-\x00d@\x08\x00\x00\x7f\x010\x00F@\x08 \x00\x02\x02\x01\x00\x01\x00d\x7f\x0c<\x00\x00@ \x00\x00\x01\x07\x0066\x08\x05d\x00A\x7f^@\x04.\x00\x7f\x005\x01r\x00@\x08\x00\x00\x00C\x00\x00F@2\x00\x02\x01\x07\x00\x00\x02P\x7f\x0cv\x00\x08\x00@\x00\x00\x01\x07\x01\x0299\x05d\x004\x00\x00\x7f@(\x00\x7f\x004\x00\x00d@\x08\x00\x7f\x00\x005\x7f?@(\x00\x02 \x01\x07\x7f\x02Z\x7f\x0c\x02v\x00\x00@\x00\x00\x01\x00\x7f\x7f66\x7f\x7f\x00f\x00\x00n@\x14\x00\x00\x00\x00-\x00d@\x08\x00\x00\x7f\x00\x04\x7fc@2\x08\x00\x02\x01\x01\x00\x02P\x00\x7f\x0c\x7f\x00\x00@\x00P\x00\x01\x00\x0066\x05\x00d\x01O\x00h@\x1c\x00\x00\x00\x00-\x00d@\x00\x08\x00\x00\x005\x00F\x00@ \x00\x02\x02\x01\x00\x00\x01d\x7f\x0c<\x00\x00\x10@\x00\x00\x01\x0f\x007\x007\x05d\x00m\x00p\x00@("\x00\x00\x06\x00\x00d@\x08\x00\x7f\x004\x00\x00F@$\x00\x02\x03\x00\x01\x00\x01P\x7f\x0cD\x04\x00\x00@\x00\x00\x01\x7f\x01\x7f\x00\x00\x7f\x7f\x00\x05M~\x7f\x7fN%\x00\x01@\x00\x01\x00\x00\x16K\x7f\x00\x01m\x01\n[ \x7f \x0c\r\t\x7f\x05\x7f\x7f\x01\x01\x7f\x00\x00@\x00\x00 \x01\x00\x0099\x05d\x00\x01o\x7f\x7f@\x1c\x00\x10\x7f\x005\x00d@\x08\x00\x00\x7f\x004\x00_@\x00 \x00\x02\x02\x01\x00\x01\x00d\x7f\x0c<\x00\x00@ \x00\x00\x01\x00\x0099\x00\x05d\x00!\x00h@\x08\x1c\x00\x00\x00-\x00d\x00@\x08\x00\x7f\x00f\x00\x00F@ \x00\x02\x02\x01\x00\x00\x01d\x7f\x0c<\x00\x08\x00@\x00\x00\x01\x00\x00\x0099\x05d\x00A\x00\x00^@.\x00\x7f\x00\x1b\x00\x00/@\x08\x00\x7f\x00\x00C\x7fF@2\x00\x02 \x02\x01\x00\x02P\x7f\x0c\x02<\x00\x00@\x00\x00\x01\x00\x00\x0066\x05d\x00\x005\x00V@(\x00\x00\x00\x00-\x00d@\x08\x00\x00\x7f\x00W\x00Y@(\x00\x1e\x02\x02\x01\x00\x01Z\x00\x7f\x0c<\x00\x00@\x00@\x00PSR\x03\x00\x00\x00b\xf7\xf0Cs\x7fD\x06\t\x00\x01\x00\x01\x7f\x7f\x7f\xf7'
,{
    'Style number': None,
    'Accompaniment': None,
    'Split Point': 0,
    'Main A/B': None,
    'Style Volume': None,
    'Tempo': None,
    'Main Voice number': 134,
    'M. Volume': 127,
    'M. Octave': -2,
    'M. Pan': 127,
    'M. Reverb Level': 78,
    'M. Chorus Level': 37,
    'Dual Voice number': 494,
    'Dual': 'ON',
    'D. Volume': 10,
    'D. Octave': +1,
    'D. Pan': 91,
    'D. Reverb Level': 32,
    'D. Chorus Level': 127,
    'Split Voice number': 257,
    'Split': 'OFF',
    'S. Volume': 0,
    'S. Octave': +1,
    'S. Pan': 0,
    'S. Reverb Level': 22,
    'S. Chorus Level': 75,
    'Reverb Type': '-- Plate',
    'Chorus Type': '-- Flanger',
    'Sustain': 'OFF',
    'Harmony': 'ON',
    'Harmony Type': '05 Octave',
    'Harmony Volume': 127,
    'Transpose': -11,
    'Pitch Bend Range': 12
})]

def test_reg():
    for hexdata, sets in testdata:
        infile = e.read_syx_file(io.BytesIO(hexdata))
        ddat = e.decode_section_messages(infile)
        dobj = e.RegData(ddat)
        dsets, b = dobj.get_settings(2, 4)
        assert len(b) == 0
        for key, value in sets.items():
            assert dsets[key] == value