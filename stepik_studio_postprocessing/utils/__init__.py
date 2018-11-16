import contextlib
import wave

import numpy as np

from stepik_studio_postprocessing.utils.descriptors.audio_file_descriptor import AudioFileDescriptor
from stepik_studio_postprocessing.utils.types.audio_suffixes import AudioSuffixes


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


def frames_to_seconds(frames: int, frequency: int) -> float:
    """
    Duration of frames in seconds:
    period = 1/frequency; duration = period * number_of_frames

    :param frames: number of frames
    :param frequency: frequency of signal in hertz (Hz)
    :return: duration in seconds
    """
    return frames / frequency


def seconds_to_frames(seconds: float, frequency: int) -> int:
    """
    Seconds to number of frames:
    period = 1/frequency
    number_of_frames = duration_in_seconds / period = frequency_of_signal * duration_in_seconds

    :param seconds: seconds in float
    :param frequency: frequency of expected signal in hertz (Hz)
    :return: duration in frames
    """

    return int(seconds * frequency)


def get_chunk(audio_fd: AudioFileDescriptor, chunksize: int = 10000):
    """
    :param audio_fd: AudioFileDescriptor of WAV file
    :param chunksize: number of frames to return
    :return: Numpy array of numpy.int32 with chunksize size
    """
    if not is_compatible(audio_fd, [AudioSuffixes.WAV]):
        raise TypeError('Provides only WAV files processing. {} is not compatible'.format(audio_fd.audio_type))

    with contextlib.closing(wave.open(audio_fd.path, 'r')) as f:
        chunk = f.readframes(chunksize)

    return np.fromstring(chunk, audio_fd.get_sample_size())


def is_compatible(audio_fd: AudioFileDescriptor, allowable_suffixes: list) -> bool:
    """
    Checks that type of audio which represented by AudioFileDescriptor is allowable

    :param audio_fd: AudioFileDescriptor
    :param allowable_suffixes: list of allowable audio extensions
    :return: bool
    """

    return audio_fd.audio_type in allowable_suffixes
