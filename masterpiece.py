# -*- coding: utf-8 -*-

from midiutil.MidiFile import MIDIFile
from randomnote import RandomNote


class Masterpiece(object):
    def __init__(self, rules, rhythm, length, tempo):
        self.length = length
        self.tempo = tempo
        self.rhythm = rhythm

        self.rules = rules
        self.rn = RandomNote(rules['notes'], rules['interval_upper'], rules['interval_lower'])

        self.MyMIDI = MIDIFile(3)
        self.current_track_number = 0

    def create_melody_sequence(self):
        seq_melody = []
        lilypond_str = '\\header {\n    title = "Note Reading Exercises"\n}\n'
        lilypond_str += '\\version "2.18.2"\n\n'

        for i in range(self.length):
            for phrase in self.rhythm:
                lilypond_str += '{\n    \\time 4/4\n    '
                lilypond_str += '\\key c \\major\n    '
                self.rn.reset()
                for duration in phrase:
                    note = self.rn.random_note()
                    seq_melody.append((note, duration))
                    note_index = self.rules['notes'].index(note)
                    offset = note_index % 7
                    note_name = chr(ord('a') + (offset + 2) % 7)
                    #note_name += 'is'
                    note_name += "'" * (note_index // 7 + 1)
                    lilypond_str += f'{note_name} '
                lilypond_str += '\n}\n'

        return seq_melody, lilypond_str

    def create_melody_track(self):
        seq_melody, lilypond_str = self.create_melody_sequence()

        self.MyMIDI.addTrackName(
            track=self.current_track_number,
            time=0, trackName='piano')
        self.MyMIDI.addTempo(
            track=self.current_track_number,
            time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(
            tracknum=self.current_track_number,
            channel=0, time=0, program=0)

        pos = 4
        for pitch, duration in seq_melody:
            relative_pos = pos - int(pos / 4) * 4
            if 0 <= relative_pos < 1:
                vol = self.rules['velocity']['strong']
            elif 2 <= relative_pos < 3:
                vol = self.rules['velocity']['intermediate']
            else:
                vol = self.rules['velocity']['weak']
            self.MyMIDI.addNote(
                track=self.current_track_number,
                channel=0, pitch=pitch, time=pos, duration=duration, volume=vol)
            if relative_pos in [0, 2]:
                self.MyMIDI.addControllerEvent(
                    track=self.current_track_number,
                    channel=0, time=pos, controller_number=64, parameter=127)
                self.MyMIDI.addControllerEvent(
                    track=self.current_track_number,
                    channel=0, time=pos + 1.96875, controller_number=64, parameter=0)
            pos += duration
        self.current_track_number += 1

        return lilypond_str

    def create_midi_file(self, filename):
        lilypond_str = self.create_melody_track()
        with open(filename, 'wb') as midi_file:
            self.MyMIDI.writeFile(midi_file)

        return lilypond_str
