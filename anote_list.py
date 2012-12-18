# -*- coding: utf-8 -*-

import copy
import re

class AnoteList(list):
    """Anoteインスタンスを格納するリスト

    ルール適用の際に、正規表現を使うので、
    歌詞上のインデックス <=> AnoteList上のインデックス
    みたいな処理がある

    Inherits:
        list
    Attributes:
        lyrics: 格納されているAnoteインスタンス間の歌詞を連結したもの
        phonetic: 格納されているAnoteインスタンス間の発音記号を連結したもの
        relative_notes: 格納されているAnoteインスタンス間の相対音階
    Examples:
        anotes = AnoteList()
        antoes.append(Anote(1000, 64, u"あ"))
        anotes.append(Anote(100, 62, u"が")) # ソートされて先頭にくる
        anotes.lyrics => "があ"
        anotes.phonetics => "g aa"
        anotes.relative_notes => [0, 2]
    """

    def __init__(self, other_list=[]):
        """コンストラクタ

        Args:
            other_list: 他のAnoteインスタンスが入ったリスト、またはAnoteList
        """
        super(AnoteList, self).__init__()
        self.extend(other_list)

    def append(self, anote):
        """Anoteインスタンスを追加する

        リストのappend()と同じ挙動。追加時に、
            ・型のチェック（Anoteインスタンスであるか）
            ・時間順ソート
            ・歌詞が伸ばし棒関連の場合の処理

        Args:
            anote: 追加するAnoteインスタンス
        """
        if not anote.__class__.__name__ is 'Anote':
            raise TypeError("AnoteList support only Anote class for contents")
        #共通の参照のAnoteインスタンスを格納しない
        _anote = copy.deepcopy(anote) if anote in self else anote
        super(AnoteList, self).append(_anote)
        self.sort(key=lambda x: x.start)
        #歌詞が伸ばし棒だった場合
        if _anote.is_prolong:
            prev = self.index(_anote) - 1
            if prev >= 0:
                _anote.phonetic = self[prev].phonetic[-1]
        #挿入したAnoteの次の歌詞が伸ばし棒だった場合
        if self[-1] != _anote:
            next = self.index(_anote) + 1
            if self[next].is_prolong:
                self[next].phonetic = _anote.phonetic[-1]

    def extend(self, other_list):
        """他のAnoteインスタンスのリスト、AnoteListを連結する

        Args:
            other_list: 他のAnoteインスタンスのリスト、またはAnoteList
        """
        for anote in other_list:
            self.append(anote)

    def filter(self, start=None, end=None,
            lyric_start=None, lyric_end=None):
        """フィルタリングを行う

        Args:
            start: 選択始端時間
            end: 選択終端時間
            lyric_start: lyrics上の選択始端インデックス
            lyric_end: lyrics上の選択終端インデックス
            etc... 今後なにか追加できれば
        Returns:
            フィルタリングされたAnoteList
            戻り値のAnoteListは呼び出し元のものとは独立しているが、
            中身のAnoteインスタンスは共有される
        """
        s = start if start else 0
        e = end if end else self[-1].end
        lyric_s = lyric_start if lyric_start else 0
        lyric_e = lyric_end if lyric_end else len(self.lyrics)
        l2i = self.__lyric_index2index
        temp = self[l2i(lyric_s):l2i(lyric_e)]
        temp = [a for a in temp if s <= a.end and a.start <= e]
        return AnoteList(temp)

    def filter2(self, formula):
        return AnoteList(filter(formula, self))

    def map(self, formula):
        map(formula, self)
        return self

    def lyric_index(self, anote):
        """歌詞文字列上のインデックスを取得する

        Args:
            anote: 対象となるanote
        Returns:
            歌詞文字列上のインデックス
        Examples:
            anotes = AnoteList([
                Anote(10, 50, u"ちゃ"),
                Anote(20, 50, u"ちゅ"),
                Anote(30, 50, u"ちょ")])
            anote = Anote(40, 50, u"あ")
            anotes.index(anote) => 3
            anotes.lyric_index(anote) => 6
        """
        i = self.index(anote)
        string = u''.join([a.lyric for a in self[:i]])
        return i + len(re.findall(u"[ぁぃぅぇぉゃゅょ]", string))

    def split(self, distance=50):
        """distance時間以上離れているAnoteで区切る

        Args:
            distance: 区切る場所となる音符間の時間間隔
        Returns:
            区切られたAnoteList（AnoteListのList）
        """
        anote_lists = []
        buf = 0
        for i, a in enumerate(self[1:]):
            if a.start - self[i].end > distance:
                anote_lists.append(self[buf:i + 1])
                buf = i + 1
        anote_lists.append(self[buf:])
        return anote_lists

    def __lyric_index2index(self, i):
        return i - len(re.findall(u"[ぁぃぅぇぉゃゅょ]", self.lyrics[:i]))

    def __getslice__(self, i, j):
        return AnoteList(super(AnoteList, self).__getslice__(i, j))

    @property
    def lyrics(self):
        return u''.join([a.lyric for a in self])

    @property
    def phonetics(self):
        return u''.join([a.phonetic for a in self])

    @property
    def relative_notes(self):
        return [0] + [a.note-self[i].note for i,a in enumerate(self[1:])]
