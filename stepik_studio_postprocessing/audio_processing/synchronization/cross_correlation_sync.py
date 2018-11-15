import contextlib
import wave

import numpy as np

from scipy.signal import correlate
from scipy.ndimage.interpolation import shift

from stepik_studio_postprocessing.utils import normalize_signal, frames_to_seconds, get_output_waveform


class CorrelationSynchronizer(object):
    def __init__(self, chunksize: int = 10000):
        self.chunksize = chunksize

    def process(self, audio_1, audio_2, output_file: str):
        diff = self.get_frames_diff(audio_1, audio_2)

        if diff <= 0:
            source = wave.open(audio_1.path, 'r')
        else:
            source = wave.open(audio_2.path, 'r')

        output = get_output_waveform(output_file,
                                     source.getnchannels(),
                                     source.getsampwidth(),
                                     source.getframerate())

        original = source.readframes(self.chunksize)
        silence = np.zeros(abs(diff), np.int32)
        silence = np.frombuffer(silence, np.byte)

        output.writeframes(b''.join(silence))

        while original != b'':
            output.writeframes(b''.join(np.frombuffer(original, np.byte)))
            original = source.readframes(self.chunksize)

        source.close()
        output.close()

    def get_seconds_diff(self, audio_1, audio_2) -> float:
        return frames_to_seconds(self.get_frames_diff(audio_1, audio_2),
                                 audio_1.get_framerate())

    def get_frames_diff(self, audio_1, audio_2) -> int:
        wf_1 = wave.open(audio_1.path, 'r')
        wf_2 = wave.open(audio_2.path, 'r')

        frames_1 = wf_1.readframes(self.chunksize)
        frames_2 = wf_2.readframes(self.chunksize)

        frames_1 = np.fromstring(frames_1, np.int32)
        frames_2 = np.fromstring(frames_2, np.int32)

        frames_1 = normalize_signal(frames_1)
        frames_2 = normalize_signal(frames_2)

        corr = correlate(frames_1, frames_2)
        lag = np.argmax(corr)

        wf_1.close()
        wf_2.close()

        return lag - self.chunksize
