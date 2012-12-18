# -*- coding: utf-8 -*-

from anote_list import AnoteList
from anote import *
from aeks import aeks
import xml.etree.ElementTree as ET
import autochorus.MAutoChorus as MAC
 
class V3Editor(object):
    """ V3Editorのファイル(vsqx)を扱うクラス
    """
 
    def __init__(self, vsqx, part):
        """
        Args:
            vsqx:   file
            part:   int
        """
        self._part = part
        self._vsqx = (vsqx)
        self.parse()
 
    def parse(self):
        """ vsqxファイルを受け取ってコーラスのを返す
        Rets:
            XMLファイルの文字列
        """
        elem = ET.fromstring(self._vsqx)
        xmlns = '{http://www.yamaha.co.jp/vocaloid/schema/vsq3/}'
 
        masterTrack = elem.find(xmlns+"masterTrack")
        timeSig = masterTrack.find(xmlns+"timeSig")
        vsTrack = elem.find(xmlns + "vsTrack")
        musicalPart = vsTrack.find(xmlns + "musicalPart")
 
        self._nn = int(timeSig.findtext(xmlns+"nume"))
        self._dd = int(timeSig.findtext(xmlns+"denomi"))
 
        anotes = AnoteList()
        for i, note in enumerate(musicalPart.findall(xmlns+"note")):
            time=note.findtext(xmlns+"posTick")     #相対開始時間
            length=note.findtext(xmlns+"durTick")   #音の長さ
            anote=note.findtext(xmlns+"noteNum")    #音の高さ
            anotes.append(Anote(int(time), int(anote), length=int(length)))
 
        soprano_notes = [n.note for n in anotes]
        packed = MAC.execAutoChorus(anotes, aeks(soprano_notes),
                                    self._nn, self._dd)[self._part]
        notes = [] 
        for p in packed:
            notes.append(p.note)

        for i, note in enumerate(musicalPart.findall(xmlns+"note")):
            noteNum = note.find(xmlns+"noteNum")
            noteNum.text = str(notes[i])

        #return ET.dump(elem)
        return ET.tostring(elem)

"""
### FOR DEBUG
if __name__ == "__main__":
    _data = open("../vsqx/kirakira.vsqx", "rt").read()
    print V3Editor(_data, 1).parse()
"""
