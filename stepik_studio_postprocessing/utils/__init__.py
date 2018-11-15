import contextlib
import wave

import numpy as np


def get_output_waveform(output_path: str, channels, sample_width, output_framerate):
    """
    Opens waveform for writing

    :param output_framerate: frequency of output waveform
    :param sample_width: output audio bit depth
    :param channels: number of output channels
    :param output_path: path to output file
    :return: Wave_write
    """

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sample_width)
    wf.setframerate(output_framerate)
    return wf


def normalize_signal(signal):
    """
    Normalize signal to [-1, 1] range.

    :param signal: 1-D numpy array
    :return: normalized 1-D numpy array
    """

    return signal / np.amax(signal)


def frames_to_seconds(frames: int, framerate: int) -> float:
    """
    Duration of frames in seconds:
    period = 1/frequency; duration = period * number_of_frames

    :param frames: number of frames
    :param framerate: frequency of signal
    :return: duration in seconds
    """
    return frames / framerate


def get_chunk(audio_fd, chunksize: int = 10000):
    with contextlib.closing(wave.open(audio_fd.path, 'r')) as f:
        chunk = f.readframes(chunksize)

    return np.fromstring(chunk, np.int32)
