# -*- coding: utf-8 -*-

import copy
import autochorus.MAutoChorus as MAutoChorus
import autochorus.MChord as MChord
import autochorus.MUnderThree as MUnderThree
import aeks

class LyricCard(object):
    """Generate Lyric Card
    """

    def __init__(self, anotes, nn, dd):
        self._nn = nn
        self._dd = 2 ** dd
        self._anotes = copy.deepcopy(anotes)
        soprano_notes = [anote.note for anote in self._anotes]
        self._key = aeks.aeks(soprano_notes)
        self._lyrics = []
        self._chords = []
        self.__chord_and_length()

    def __chord_and_length(self):
        #分解脳を拍子の分母(?)で割りますー(全音＝1920)
        self._minimumunit = 1920 / self._nn
        qNList = MAutoChorus.noteQuantization(self._anotes, self._minimumunit)
        hamList = MAutoChorus.melodyrestoration(self._anotes, qNList, self._key, self._dd, self._nn)
        MChord.autoChord(hamList)
        MUnderThree.autoUnderThree(hamList)
        self._CLList = [{'Chord': ham.chord, 'Length': ham.length} for ham in hamList]
        self.__list_lyric()
        self.__list_chord()

    def __convert_scale(self, chord):
        if chord == 0: return ' '
        return [ {},
            # chord=> 1
            { -12: 'Bm', -11: 'Bbm', -10: 'Am', -9: 'Abm', -8: 'Gm',  -7: 'F#m',
              -6: 'Fm',  -5: 'Em',   -4: 'Ebm',-3: 'Dm',  -2: 'C#m', -1: 'Cm',
              1: 'C',    2: 'C#',    3: 'D',   4: 'Eb',   5: 'E',    6: 'F',
              7: 'F#',   8: 'G',     9: 'Ab', 10: 'A',   11: 'Bb',  12: 'B'},
            # chord=> 2
            { -12: 'C#dim', -11: 'Cdim',-10: 'Bdim',-9: 'Bbdim', -8: 'Adim',  -7: 'G#dim',
              -6: 'Gdim',  -5: 'F#dim', -4: 'Fdim', -3: 'Edim',  -2: 'D#dim', -1: 'Ddim',
              1: 'Dm',     2: 'D#m',    3: 'Em',    4: 'Fm',     5: 'F#m',    6: 'Gm',
              7: 'G#m',    8: 'Am',     9: 'Bbm',   10: 'Bm',    11: 'Cm',    12: 'C#m'},
            # chord=> 3
            { -12: 'D',  -11: 'Db', -10: 'C',  -9: 'B',   -8: 'Bb',  -7: 'A',
              -6: 'Ab',  -5: 'G',   -4: 'Gb', -3: 'Fm',  -2: 'E',   -1: 'Eb',
              1: 'Em',   2: 'Fm',   3: 'F#m', 4: 'Gm',   5: 'G#m',  6: 'Am',
              7: 'A#m',  8: 'Bm',   9: 'Cm', 10: 'C#m', 11: 'Dm',  12: 'D#m'},
            # chord=> 4
            { -12: 'Em',  -11: 'Ebm', -10: 'Dm',  -9: 'Dbm', -8: 'Cm',  -7: 'Bm',
              -6: 'Bbm',  -5: 'Am',   -4: 'Abm', -3: 'Gm',  -2: 'F#m', -1: 'Fm',
              1: 'F',     2: 'F#',    3: 'G',    4: 'Ab',   5: 'A',    6: 'Bb',
              7: 'B',     8: 'C',     9: 'Db',  10: 'D',   11: 'Eb',  12: 'E'},
            # chord=> 5
            { -12: 'F#', -11: 'F', -10: 'E',  -9: 'Eb', -8: 'D',  -7: 'C#',
              -6: 'C',   -5: 'B',  -4: 'Bb', -3: 'A',  -2: 'G#', -1: 'G',
              1: 'G',    2: 'G#',  3: 'A',   4: 'Bb',  5: 'B',   6: 'C',
              7: 'C#',   8: 'D',   9: 'Eb', 10: 'E',  11: 'F',  12: 'F#'},
            # chord=> 6
            { -12: 'G',  -11: 'Gb', -10: 'F', -9: 'E',    -8: 'Eb',  -7: 'D',
              -6: 'Db',  -5: 'C',   -4: 'B', -3: 'Bb',   -2: 'A',   -1: 'Ab',
              1: 'Am',   2: 'A#m',  3: 'Bm', 4: 'Cm',    5: 'C#m',  6: 'Dm',
              7: 'D#m',  8: 'Em',   9: 'Fm', 10: 'F#m', 11: 'Gm',  12: 'G#m'},
            # chord=> 7
            { -12: 'A',   -11: 'Ab',  -10: 'G',    -9: 'Gb',    -8: 'F',    -7: 'E',
              -6: 'Eb',   -5: 'D',    -4: 'Db',   -3: 'C',     -2: 'B',    -1: 'Bb',
              1: 'Bdim',  2: 'Cdim',  3: 'C#dim', 4: 'Ddim',   5: 'D#dim', 6: 'Edim',
              7: 'Fdim',  8: 'F#dim', 9: 'Gdim', 10: 'G#dim', 11: 'Adim', 12: 'A#dim'}][chord][self._key]

    def __list_lyric(self):
        current_locate = self._anotes[0].start / self._minimumunit
        beat = current_locate % self._nn
        measure = [' ' for i in range(beat)]
        for anote in self._anotes:
            delta_beat = anote.start / self._minimumunit - current_locate
            if delta_beat == 0 and len(measure) != 0 and measure[-1].isspace() == False:
                measure[-1] += anote.lyric.encode('utf-8')
                continue
            elif delta_beat > 1 and delta_beat + beat <= self._nn:
                measure.extend([' ' for i in range(delta_beat - 1)])
            elif delta_beat > 1 and delta_beat + beat > self._nn:
                measure.extend([' ' for i in range(self._nn - beat - 1)])
                self._lyrics.append(measure)
                measure = [' ' for i in range(delta_beat + beat - self._nn)]
                beat = delta_beat + beat - self._nn
                current_locate += delta_beat
                measure.append(anote.lyric.encode('utf-8'))
                continue
            for i in range(delta_beat):
                beat += 1
                if beat == self._nn:
                    beat = 0
                    self._lyrics.append(measure)
                    measure = []
            current_locate += delta_beat
            measure.append(anote.lyric.encode('utf-8'))
        if len(measure) != 0:
            self._lyrics.append(measure)

    def __list_chord(self):
        measure = []
        beat = 0
        pre_chord = -1 # init
        for CL in self._CLList:
            if pre_chord != CL['Chord']:
                measure.append(self.__convert_scale(CL['Chord']))
                pre_chord = CL['Chord']
            else: # when previous chord is same
                measure.append(' ')
            for L in range(CL['Length']):
                beat += 1
                if L != 0:
                    measure.append(' ')
                if beat == self._nn:
                    self._chords.append(measure)
                    measure = []
                    beat = 0
        if len(measure) != 0:
            self._chords.append(measure)
        lyric_start_measure = self._anotes[0].start / 1920
        del self._chords[0:lyric_start_measure]

    def generate(self):
        card = ''
        ColumnNum = 4
        chord_text = ['' for i in range(len(self._chords) / ColumnNum + 1)]
        lyric_text = ['' for i in range(len(self._lyrics) / ColumnNum + 1)]
        for j, msr in enumerate(self._chords):
            chord_text[j / ColumnNum] += '|'
            for i, chord in enumerate(msr):
                chord_text[j / ColumnNum] += chord + '\t'
        for j, msr in enumerate(self._lyrics):
            lyric_text[j / ColumnNum] += '|'
            for i, lyric in enumerate(msr):
                lyric_text[j / ColumnNum] += lyric + '\t'
        for i in range(len(self._chords) / ColumnNum):
            card += chord_text[i] + '\n'
            card += lyric_text[i] + '\n'
            card += '\n'
        return card
