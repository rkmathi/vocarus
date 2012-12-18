# -*- coding: utf-8 -*-

import re
import tools
from anote_list import *

class Anote(object):
    """音符イベントを扱うクラス

    ビブラート周りを除いて数値になるべきところは数値として扱う

    Attributes:
        start: イベント始端時間
        end: イベント終端時間
        length: イベントの長さ
        lyric: 歌詞
        phonetic: 発音記号
        dynamics: ベロシティ（VEL）
        vibrato: ビブラート情報（ディクショナリ）
            {"IconID": ビブラートの形式を識別するID,
             "IDS": ビブラートの形式名,
             "Caption": 不明,
             "Original": 不明,
             "Length": ビブラートの長さ,
             "StartDepth": 振幅の開始位置,
             "DepthBPNum": 振幅カーブのデータ点数,
             "DepthBPX": 振幅カーブのデータ点（時間軸）(csv),
             "DepthBPY": 振幅カーブのデータ点(csv),
             "StartRate": 周期の開始位置,
             "RateBPNum": 周期カーブのデータ点数,
             "RateBPX": 周期カーブのデータ点（時間軸）（csv),
             "RateBPY": 周期カーブのデータ点（csv)}
        prop: 音符のプロパティ（ディクショナリ）
            {"PMBendDepth": ベンドの深さ,
             "PMBendLength": ベンドの長さ,
             "PMbPortamentoUse":
                「〜形でポルタメントを付加」の指定内容
                「上行形で〜」が指定されていれば+1
                「下行形で〜」が指定されていれば+2,
             "DEMdecGainRate" ディケイ,
             "DEMaccend": アクセント}
        is_prolong: 歌詞が伸ばし棒かどうか
        event: テキストベントの形式にフォーマットされたディクショナリ
        lyric_event: 同上。歌詞イベントを扱う
    """

    # Default properties
    d_prop = {
            'PMBendDepth': 8,
            'PMBendLength': 0,
            'PMbPortamentoUse': 0,
            'DEMdecGainRate': 50,
            'DEMaccent': 50}
    _lyric = ''
    _phonetic = ''
    _length = 0
    _end = 0
    _start = 0
    _is_prolong = False  # 伸ばし棒かどうか

    def __init__(self, time, note, lyric=u"a", length=120,
                 dynamics=64, vibrato=None, prop=d_prop):
        self.start = time
        self.note = note
        self.length = length
        self.lyric = lyric
        self.dynamics = dynamics
        self.vibrato = vibrato
        self.prop = prop

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return tools.pp_str({
                "start": self.start,
                "end": self._end,
                "note": self.note,
                "length": self._length,
                "lyric": self._lyric,
                "dynamics": self.dynamics,
                "properties": self.prop
                })

    def set_lyric(self, lyric):
        self._lyric = lyric
        self._is_prolong = bool(re.match(u"[-ー−]", self._lyric))
        self._phonetic = tools.lyric2phonetic(lyric)

    def get_lyric(self):
        return self._lyric

    def set_phonetic(self, phonetic):
        self._phonetic = phonetic
        #歌詞が伸ばし棒の時は発音記号の同期をしない
        if not self._is_prolong:
            self._lyric = tools.phonetic2lyric(phonetic)

    def get_phonetic(self):
        return self._phonetic

    def set_length(self, length):
        self._length = length
        self._end = self.start + length

    def get_length(self):
        return self._length

    def set_start(self, start):
        self._start = start
        self._end = self.start + self.length

    def get_start(self):
        return self._start

    def set_end(self, end):
        self._end = end
        self._length = end - self._start

    def get_end(self):
        return self._end
    lyric = property(get_lyric, set_lyric)
    phonetic = property(get_phonetic, set_phonetic)
    length = property(get_length, set_length)
    start = property(get_start, set_start)
    end = property(get_end, set_end)

    @property
    def is_prolong(self):
        return self._is_prolong

    @property
    def event(self):
        """音符イベント形式の音符データを取得する

        Returns:
            音符イベント形式の音符データ
            数値も文字列として格納される
        """
        event = {
            'Type': 'Anote',
            'time': str(self.start),
            'Length': str(self.length),
            'Note#': str(self.note)}
        for key, value in self.prop.items():
            self.prop[key] = str(value)
        event.update(self.prop)
        if self.vibrato:
            vd = int((1 - int(self.vibrato['Length'])/100.0)*self.length/5) * 5
            event['VibratoDelay'] = str(vd)
        return event

    @property
    def lyric_event(self):
        """詳細イベント形式の歌詞データを取得する

        Returns:
            詳細イベント形式の歌詞データ
            数値も文字列として格納される
        """
        lyric_event = {
            'lyric': self._lyric.encode('shift-jis'),
            'phonetic': self._phonetic.encode('shift-jis'),
            'lyric_delta': "%.6f" % 0,
            'protect': "0"}
        #ConsonantAdjustmentを追加
        phonetics = self._phonetic.split(' ')
        boinrxp = re.compile('aiMeo')
        for i, p in enumerate(phonetics):
            lyric_event['ca' + str(i)] = 0 if boinrxp.match(p) else 64
        return lyric_event

    @property
    def vibrato_event(self):
        """詳細イベント形式のビブラートデータを取得する

        Returns:
            詳細イベント形式の歌詞データ
        """
        return self.vibrato
