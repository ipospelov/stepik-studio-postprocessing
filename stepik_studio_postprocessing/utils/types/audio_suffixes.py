from enum import Enum


class AudioSuffixes(Enum):
    MP3 = '.mp3'
    WAV = '.wav'
    ODT = '.odt'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
