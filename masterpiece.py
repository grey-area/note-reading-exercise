# -*- coding: utf-8 -*-

from midiutil.MidiFile import MIDIFile
from randomnote import RandomNote


class Masterpiece(object):
    c_major_scale = [33, 35, 36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]
    offsets = {'a': -3, 'b': -1, 'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7}

    def __init__(self, rules, rhythm, args):
        self.length = args.num_exercises
        self.tempo = args.tempo
        self.rhythm = rhythm

        self.key = args.key
        self.offset = Masterpiece.offsets[self.key[0]]
        if len(self.key) == 3:
            if self.key[1:] == 'es':
                self.offset -= 1
            else:
                self.offset += 1

        self.notes = [note + self.offset for note in Masterpiece.c_major_scale if note + self.offset >= 48 and note + self.offset <= 72]

        self.rules = rules
        self.rn = RandomNote(self.notes, rules['interval_upper'], rules['interval_lower'])

        self.MyMIDI = MIDIFile(3)

    def create_melody_sequence(self):
        seq_melody = []
        lilypond_str = '\\version "2.18.2"\n\n'
        lilypond_str += '\\header {\n    title = "'
        lilypond_str += f'Note Reading Exercises in {self.key[0].upper()}'
        if len(self.key) == 3:
            if self.key[1:] == 'is':
                lilypond_str += '♯'
            else:
                lilypond_str += '♭'
        lilypond_str += ' Major'
        lilypond_str += '"\n}\n\n'

        for i in range(self.length):
            for phrase in self.rhythm:
                lilypond_str += '{\n    \\time 4/4\n    '
                lilypond_str += '\\key c \\major\n    '
                lilypond_str += '\\transpose c '
                lilypond_str += self.key
                if self.key[0] in 'ab':
                    lilypond_str += ','
                lilypond_str += ' {\n        '
                self.rn.reset()
                for duration in phrase:
                    note = self.rn.random_note()
                    seq_melody.append((note, duration))
                    note_index = Masterpiece.c_major_scale.index(note - self.offset)
                    offset = note_index % 7
                    note_name = chr(ord('a') + offset % 7)
                    note_name += "'" * ((note_index - 2) // 7)
                    lilypond_str += f'{note_name} '
                lilypond_str += '\n    }\n}\n'

        return seq_melody, lilypond_str

    def create_melody_track(self):
        seq_melody, lilypond_str = self.create_melody_sequence()

        self.MyMIDI.addTrackName(track=0, time=0, trackName='piano')
        self.MyMIDI.addTempo(track=0, time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(tracknum=0, channel=0, time=0, program=0)

        pos = 4
        for pitch, duration in seq_melody:
            relative_pos = pos - int(pos / 4) * 4
            if 0 <= relative_pos < 1:
                vol = self.rules['velocity']['strong']
            elif 2 <= relative_pos < 3:
                vol = self.rules['velocity']['intermediate']
            else:
                vol = self.rules['velocity']['weak']
            self.MyMIDI.addNote(track=0, channel=0, pitch=pitch,
                                time=pos, duration=duration, volume=vol)
            if relative_pos in [0, 2]:
                self.MyMIDI.addControllerEvent(track=0, channel=0, time=pos,
                                               controller_number=64, parameter=127)
                self.MyMIDI.addControllerEvent(track=0, channel=0, time=pos + 1.96875,
                                               controller_number=64, parameter=0)
            pos += duration

        return lilypond_str

    def create_midi_file(self, filename):
        lilypond_str = self.create_melody_track()
        with open(filename, 'wb') as midi_file:
            self.MyMIDI.writeFile(midi_file)

        return lilypond_str
