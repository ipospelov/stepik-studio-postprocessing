# Original code:
# https://github.com/loehnertz/rattlesnake

import logging
import wave

import numpy as np

from stepik_studio_postprocessing.utils import get_output_waveform
from stepik_studio_postprocessing.utils.descriptors.audio_file_descriptor import AudioFileDescriptor
from stepik_studio_postprocessing.utils.types.audio_suffixes import AudioSuffixes

logger = logging.getLogger(__name__)


class AdaptiveNoiseCanceller(object):
    def __init__(self, output_framerate=None,
                 channels=None,
                 sample_width=None,
                 ratio: float = 1.0,
                 chunk_size: int = 4096):
        self.output_framerate = output_framerate
        self.channels = channels
        self.sample_width = sample_width
        self.ratio = ratio
        self.chunk_size = chunk_size

    def process(self, main_audio, aux_audio, output_file: str):
        """
        Mixes main audio file with inverted auxiliary audio file to cancel background noise.
        :param main_audio: AudioFileDescriptor of main audio
        :param aux_audio: AudioFileDescriptor of auxiliary audio
        :param output_file: Path to output file
        :return: AudioFileDescriptor of result file
        """
        if main_audio.audio_type is not AudioSuffixes.WAV:
            logger.error('Wrong type of audio file')
            raise TypeError('Type of main audio file should be {} instead of {}'
                            .format(AudioSuffixes.WAV, main_audio.audio_type))

        if aux_audio.audio_type is not AudioSuffixes.WAV:
            logger.error('Wrong type of audio file')
            raise TypeError('Type of auxiliary audio file should be {} instead of {}'
                            .format(AudioSuffixes.WAV, aux_audio.audio_type))

        main_wf = wave.open(main_audio.path, 'r')
        aux_wf = wave.open(aux_audio.path, 'r')

        if not self.output_framerate:
            self.output_framerate = main_wf.getframerate()

        if not self.sample_width:
            self.sample_width = main_wf.getsampwidth()

        if not self.channels:
            self.channels = main_wf.getnchannels()

        output_wf = get_output_waveform(output_file,
                                        self.channels,
                                        self.sample_width,
                                        self.output_framerate)

        original = main_wf.readframes(self.chunk_size)
        aux = aux_wf.readframes(self.chunk_size)

        while original != b'' and aux != b'':
            inverted_aux = self._invert(aux)
            mix = self._mix_samples(original, inverted_aux)
            output_wf.writeframes(b''.join(mix))

            original = main_wf.readframes(self.chunk_size)
            aux = aux_wf.readframes(self.chunk_size)

        output_wf.close()
        main_wf.close()
        aux_wf.close()

        return AudioFileDescriptor(output_file)

    def _check_compatibility(self, main_wf, aux_wf):
        """
        Checks framerate compability of input files. It must be the same.
        :param main_wf: Waveform of main audio file
        :param aux_wf: Waveform of auxiliary audio file
        """
        if main_wf.getframerate() != aux_wf.getframerate():
            logger.error('Input audio files must have the same framerate')
            raise ValueError('Input audio files must have the same framerate')

        if main_wf.getsampwidth() != aux_wf.getsampwidth():
            logger.warning('Input audio files have difference sample width. '
                           'This can lead to loss of quality.')

    def _invert(self, data):
        """
        Inverts the byte data it received utilizing an XOR operation.

        :param data: A chunk of byte data
        :return inverted: The same size of chunked data inverted bitwise
        """

        intwave = np.fromstring(data, np.int32)
        intwave = np.invert(intwave)
        inverted = np.frombuffer(intwave, np.byte)

        return inverted

    def _mix_samples(self, sample_1, sample_2):
        """
        Mixes two samples into each other

        :param sample_1: A bytestring containing the first audio source
        :param sample_2: A bytestring containing the second audio source
        :return mix: A bytestring containing the two samples mixed together
        """

        (ratio_1, ratio_2) = self._get_ratios()

        intwave_sample_1 = np.fromstring(sample_1, np.int16)
        intwave_sample_2 = np.fromstring(sample_2, np.int16)

        intwave_mix = (intwave_sample_1 * ratio_1 + intwave_sample_2 * ratio_2).astype(np.int16)

        mix = np.frombuffer(intwave_mix, np.byte)
        return mix

    def _get_ratios(self):
        """
        Calculates the ratios using a received float

        :return ratio_1, ratio_2: The two calculated actual ratios
        """

        ratio = float(self.ratio)
        ratio_1 = ratio / 2
        ratio_2 = 1 - ratio_1
        return ratio_1, ratio_2
