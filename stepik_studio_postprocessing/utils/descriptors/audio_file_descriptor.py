import contextlib
import wave

import numpy as np

from stepik_studio_postprocessing.utils.descriptors.media_file_descriptor import MediaFileDescriptor
from stepik_studio_postprocessing.utils.types.audio_suffixes import AudioSuffixes
from stepik_studio_postprocessing.utils.types.media_types import MediaTypes


class AudioFileDescriptor(MediaFileDescriptor):
    sample_sizes = {
        1: np.byte,
        2: np.int16,
        4: np.int32
    }

    def __init__(self, path: str):
        super().__init__(path)

        if AudioSuffixes.has_value(self.suffix):
            self.media_type = MediaTypes.AUDIO
            self.audio_type = AudioSuffixes(self.suffix)
        else:
            raise TypeError('Audio descriptor doesn\'t support {} files'.format(self.suffix))

        self._framerate = None
        self._width = None
        self._n_channels = None

    def get_framerate(self):
        if self._framerate:
            return self._framerate
        else:
            return self._get_info()[0]

    def get_sample_width(self):
        if self._width:
            return self._width
        else:
            return self._get_info()[1]

    def get_n_channels(self):
        if self._n_channels:
            return self._n_channels
        else:
            return self._get_info()[2]

    def _get_info(self):
        with contextlib.closing(wave.open(self.path, 'r')) as f:
            self._width = f.getsampwidth()
            self._n_channels = f.getnchannels()
            self._framerate = f.getframerate()

        return self._framerate, self._width, self._n_channels

    def get_sample_size(self):
        n_bytes = self.get_n_channels() * self.get_sample_width()
        return self.sample_sizes[n_bytes]
