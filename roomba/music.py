"""
Music note constants and timing definitions for Roomba MIDI playback.

This module provides note definitions in lilypond notation and timing constants
for composing songs to play on the Roomba's built-in speaker.
"""

# Silence/rest note
REST = 30

# Note definitions - Octave 4
c4 = 60
cis4 = des4 = 61
d4 = 62
dis4 = ees4 = 63
e4 = 64
f4 = 65
fis4 = ges4 = 66
g4 = 67
gis4 = aes4 = 68
a4 = 69
ais4 = bes4 = 70
b4 = 71

# Note definitions - Octave 5
c5 = 72
cis5 = des5 = 73
d5 = 74
dis5 = ees5 = 75
e5 = 76
f5 = 77
fis5 = ges5 = 78
g5 = 79
gis5 = aes5 = 80
a5 = 81
ais5 = bes5 = 82
b5 = 83

# Note definitions - Octave 6
c6 = 84
cis6 = des6 = 85
d6 = 86
dis6 = ees6 = 87
e6 = 88
f6 = 89
fis6 = ges6 = 90

# Timing constants (in 1/64ths of a second)
# Adjust MEASURE to change overall tempo (4/4 time signature)
MEASURE = 160
HALF = MEASURE // 2
QUARTER = MEASURE // 4
EIGHTH = MEASURE // 8
EIGHTH_DOT = MEASURE * 3 // 16
SIXTEENTH = MEASURE // 16

# Legacy aliases for backwards compatibility
Q = QUARTER
E = EIGHTH
Ed = EIGHTH_DOT
S = SIXTEENTH

# Time in seconds for one measure
MEASURE_TIME = MEASURE / 64.0
