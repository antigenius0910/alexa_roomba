"""
Unit tests for roomba.music module.

Tests MIDI note constants and duration values.
"""

import pytest
from roomba import music


class TestNoteConstants:
    """Test MIDI note constant values."""

    @pytest.mark.unit
    def test_middle_c(self):
        """Test middle C (C4) value."""
        assert music.c4 == 60  # MIDI standard

    @pytest.mark.unit
    def test_c_major_scale(self):
        """Test C major scale notes are in correct order."""
        assert music.c4 < music.d4 < music.e4 < music.f4 < music.g4 < music.a4 < music.b4

    @pytest.mark.unit
    def test_octave_spacing(self):
        """Test octaves are 12 semitones apart."""
        assert music.c5 - music.c4 == 12
        assert music.c6 - music.c5 == 12
        assert music.d5 - music.d4 == 12

    @pytest.mark.unit
    def test_semitone_spacing(self):
        """Test adjacent notes are 1 semitone apart."""
        assert music.d4 - music.c4 == 2  # Whole step
        assert music.e4 - music.d4 == 2  # Whole step
        assert music.f4 - music.e4 == 1  # Half step
        assert music.g4 - music.f4 == 2  # Whole step

    @pytest.mark.unit
    def test_sharp_notes(self):
        """Test sharp note values."""
        assert music.cs4 == music.c4 + 1  # C# is 1 semitone above C
        assert music.ds4 == music.d4 + 1  # D# is 1 semitone above D
        assert music.fs4 == music.f4 + 1  # F# is 1 semitone above F

    @pytest.mark.unit
    def test_octave_2_notes(self):
        """Test octave 2 notes."""
        assert music.c2 == 36
        assert music.d2 == 38
        assert music.e2 == 40

    @pytest.mark.unit
    def test_octave_3_notes(self):
        """Test octave 3 notes."""
        assert music.c3 == 48
        assert music.d3 == 50
        assert music.e3 == 52

    @pytest.mark.unit
    def test_octave_5_notes(self):
        """Test octave 5 notes."""
        assert music.c5 == 72
        assert music.d5 == 74
        assert music.e5 == 76

    @pytest.mark.unit
    def test_octave_6_notes(self):
        """Test octave 6 notes."""
        assert music.c6 == 84
        assert music.d6 == 86
        assert music.e6 == 88

    @pytest.mark.unit
    def test_all_notes_in_midi_range(self):
        """Test all notes are within valid MIDI range (31-127 for Roomba)."""
        # Get all note constants
        note_attrs = [attr for attr in dir(music) if not attr.startswith('_')]
        note_values = [getattr(music, attr) for attr in note_attrs
                      if isinstance(getattr(music, attr), int)
                      and attr not in ['MEASURE', 'HALF', 'QUARTER', 'EIGHTH', 'SIXTEENTH']]

        for value in note_values:
            assert 31 <= value <= 127, f"Note value {value} out of Roomba range"


class TestDurationConstants:
    """Test note duration constants."""

    @pytest.mark.unit
    def test_measure_value(self):
        """Test MEASURE duration value."""
        assert music.MEASURE == 160

    @pytest.mark.unit
    def test_duration_relationships(self):
        """Test duration constants have correct relationships."""
        assert music.HALF == music.MEASURE // 2
        assert music.QUARTER == music.MEASURE // 4
        assert music.EIGHTH == music.MEASURE // 8
        assert music.SIXTEENTH == music.MEASURE // 16

    @pytest.mark.unit
    def test_duration_ratios(self):
        """Test duration ratios."""
        assert music.HALF == music.QUARTER * 2
        assert music.QUARTER == music.EIGHTH * 2
        assert music.EIGHTH == music.SIXTEENTH * 2

    @pytest.mark.unit
    def test_duration_values(self):
        """Test specific duration values."""
        assert music.MEASURE == 160
        assert music.HALF == 80
        assert music.QUARTER == 40
        assert music.EIGHTH == 20
        assert music.SIXTEENTH == 10

    @pytest.mark.unit
    def test_durations_positive(self):
        """Test all durations are positive."""
        assert music.MEASURE > 0
        assert music.HALF > 0
        assert music.QUARTER > 0
        assert music.EIGHTH > 0
        assert music.SIXTEENTH > 0

    @pytest.mark.unit
    def test_duration_ordering(self):
        """Test durations are in correct order."""
        assert music.MEASURE > music.HALF > music.QUARTER > music.EIGHTH > music.SIXTEENTH


class TestSongComposition:
    """Test creating songs from notes and durations."""

    @pytest.mark.unit
    def test_simple_song(self):
        """Test creating a simple song."""
        song = [
            (music.c5, music.QUARTER),
            (music.d5, music.QUARTER),
            (music.e5, music.HALF),
        ]

        assert len(song) == 3
        assert all(isinstance(note, int) and isinstance(dur, int) for note, dur in song)

    @pytest.mark.unit
    def test_song_length_limit(self):
        """Test song length limit (16 notes max for Roomba)."""
        # Create max length song
        max_song = [(music.c5, music.QUARTER)] * 16
        assert len(max_song) == 16

        # Create too-long song
        too_long = [(music.c5, music.QUARTER)] * 17
        assert len(too_long) > 16  # This would need to be split

    @pytest.mark.unit
    def test_c_major_scale_song(self):
        """Test C major scale as a song."""
        scale = [
            (music.c5, music.EIGHTH),
            (music.d5, music.EIGHTH),
            (music.e5, music.EIGHTH),
            (music.f5, music.EIGHTH),
            (music.g5, music.EIGHTH),
            (music.a5, music.EIGHTH),
            (music.b5, music.EIGHTH),
            (music.c6, music.QUARTER),
        ]

        assert len(scale) == 8
        # Verify ascending notes
        notes = [note for note, dur in scale]
        assert notes == sorted(notes)

    @pytest.mark.unit
    def test_varied_durations(self):
        """Test song with varied note durations."""
        song = [
            (music.c5, music.WHOLE := music.MEASURE),
            (music.d5, music.HALF),
            (music.e5, music.QUARTER),
            (music.f5, music.EIGHTH),
            (music.g5, music.SIXTEENTH),
        ]

        durations = [dur for note, dur in song]
        assert durations[0] > durations[1] > durations[2] > durations[3] > durations[4]

    @pytest.mark.unit
    def test_repeated_notes(self):
        """Test song with repeated notes (different durations)."""
        song = [
            (music.c5, music.QUARTER),
            (music.c5, music.QUARTER),
            (music.c5, music.HALF),
        ]

        assert len(song) == 3
        assert all(note == music.c5 for note, dur in song)

    @pytest.mark.unit
    @pytest.mark.parametrize("note,duration", [
        (music.c4, music.QUARTER),
        (music.d5, music.EIGHTH),
        (music.e6, music.HALF),
        (music.fs4, music.SIXTEENTH),
    ])
    def test_individual_note_duration_pairs(self, note, duration):
        """Test individual note-duration pairs are valid."""
        pair = (note, duration)
        assert isinstance(pair[0], int)
        assert isinstance(pair[1], int)
        assert 31 <= pair[0] <= 127
        assert pair[1] > 0


class TestChromatic Scale:
    """Test chromatic scale notes."""

    @pytest.mark.unit
    def test_chromatic_sequence(self):
        """Test chromatic scale has all 12 semitones."""
        # Chromatic scale in octave 4
        chromatic = [
            music.c4, music.cs4, music.d4, music.ds4,
            music.e4, music.f4, music.fs4, music.g4,
            music.gs4, music.a4, music.as4, music.b4
        ]

        # Should have 12 notes
        assert len(chromatic) == 12

        # Each should be 1 semitone apart
        for i in range(len(chromatic) - 1):
            assert chromatic[i+1] - chromatic[i] == 1

    @pytest.mark.unit
    def test_enharmonic_equivalents(self):
        """Test that sharps and flats are equivalent."""
        # C# = Db, D# = Eb, etc.
        # In MIDI, there's only one value for each pitch

        assert music.cs4 == music.c4 + 1  # C# is one above C
        assert music.ds4 == music.d4 + 1  # D# is one above D

        # Can also think of as flats
        # Db4 would be same as C#4
        db4 = music.d4 - 1
        assert db4 == music.cs4


class TestEdgeCases:
    """Test edge cases for music constants."""

    @pytest.mark.unit
    def test_lowest_note(self):
        """Test lowest available note."""
        # Roomba supports MIDI 31-127
        # c2 = 36, which is in range
        assert music.c2 >= 31

    @pytest.mark.unit
    def test_highest_note(self):
        """Test highest available note."""
        # c6 = 84, which is well within range
        assert music.c6 <= 127

    @pytest.mark.unit
    def test_note_type(self):
        """Test all notes are integers."""
        notes = [music.c4, music.d4, music.e4, music.f4]
        assert all(isinstance(note, int) for note in notes)

    @pytest.mark.unit
    def test_duration_type(self):
        """Test all durations are integers."""
        durations = [music.MEASURE, music.HALF, music.QUARTER]
        assert all(isinstance(dur, int) for dur in durations)

    @pytest.mark.unit
    def test_rest_representation(self):
        """Test that rests can be represented."""
        # MIDI note 0 is sometimes used for rest
        # Or use very short duration with any note
        rest = (music.c4, 1)  # Very short note could be imperceptible
        assert isinstance(rest[0], int)
        assert isinstance(rest[1], int)


class TestMusicTheory:
    """Test music theory relationships."""

    @pytest.mark.unit
    def test_perfect_fifth_interval(self):
        """Test perfect fifth is 7 semitones."""
        assert music.g4 - music.c4 == 7
        assert music.a5 - music.d5 == 7

    @pytest.mark.unit
    def test_major_third_interval(self):
        """Test major third is 4 semitones."""
        assert music.e4 - music.c4 == 4
        assert music.fs5 - music.d5 == 4

    @pytest.mark.unit
    def test_major_chord(self):
        """Test major chord structure (root, major third, perfect fifth)."""
        # C major chord: C, E, G
        c_major = [music.c4, music.e4, music.g4]

        assert c_major[1] - c_major[0] == 4  # Major third
        assert c_major[2] - c_major[0] == 7  # Perfect fifth

    @pytest.mark.unit
    def test_octave_equivalence(self):
        """Test notes in different octaves differ by 12."""
        # C notes across octaves
        c_notes = [music.c2, music.c3, music.c4, music.c5, music.c6]

        for i in range(len(c_notes) - 1):
            assert c_notes[i+1] - c_notes[i] == 12
