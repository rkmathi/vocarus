# -*- coding: utf-8 -*-

class Singer(object):
    """歌手変更イベントを扱うクラス

    歌手変更イベントは詳しく扱う必要がない気がするのでスルー

    Attributes:
        start: イベント発生時間
        params: 各パラメータ
    """

    def __init__(self, time, params):
        self.start = time
        self.params = params

    @property
    def event(self):
        return {'Type': 'Singer', 'time': str(self.start)}

    @property
    def singer_event(self):
        return self.params

