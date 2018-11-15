from enum import Enum


class VideoSuffixes(Enum):
    TS = '.TS'
    MP4 = '.mp4'
    MPEG4 = '.mpeg4'
    MKV = '.mkv'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
