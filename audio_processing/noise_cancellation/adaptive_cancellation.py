# Original code:
# https://github.com/loehnertz/rattlesnake

import wave
import logging

import numpy as np

# Sample width of the live recording
WIDTH = 2
CHUNK = 1
RATIO = 1.0

logger = logging.getLogger(__name__)

class AdaptiveNoiseCanceller(object):
    def __init__(self, output_framerate: int = 44100, channels: int = 2):
        self.output_framerate = output_framerate
        self.channels = channels

    def process(self, main_file: str, aux_file: str, output_file: str):
        main_wf = self.read(main_file)
        aux_wf = self.read(aux_file)
        output_wf = self.get_output_waveform(output_file)

        original = main_wf.readframes(CHUNK)
        aux = aux_wf.readframes(CHUNK)

        while original != b'' and aux != b'':
            inverted_aux = self.invert(aux)
            mix = self.mix_samples(original, inverted_aux, RATIO)
            output_wf.writeframes(b''.join(mix))

            original = main_wf.readframes(CHUNK)
            aux = aux_wf.readframes(CHUNK)

        output_wf.close()
        main_wf.close()
        aux_wf.close()

    def read(self, path):
        try:
            return wave.open(path, 'r')
        except wave.Error:
            logger.error('The program can only process wave audio files (.wav)')
            return
        except FileNotFoundError:
            logger.error('File %s does not exist', path)
            return

    def get_output_waveform(self, output_path: str):
        wf = wave.open(output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(WIDTH)
        wf.setframerate(self.output_framerate)
        return wf

    def invert(self, data):
        """
        Inverts the byte data it received utilizing an XOR operation.

        :param data: A chunk of byte data
        :return inverted: The same size of chunked data inverted bitwise
        """

        # Convert the bytestring into an integer
        intwave = np.fromstring(data, np.int32)
        # Invert the integer
        intwave = np.invert(intwave)
        # Convert the integer back into a bytestring
        inverted = np.frombuffer(intwave, np.byte)
        # Return the inverted audio data
        return inverted

    def mix_samples(self, sample_1, sample_2, ratio):
        """
        Mixes two samples into each other

        :param sample_1: A bytestring containing the first audio source
        :param sample_2: A bytestring containing the second audio source
        :param ratio: A float which determines the mix-ratio of the two samples (the higher, the louder the first sample)
        :return mix: A bytestring containing the two samples mixed together
        """

        # Calculate the actual ratios based on the float the function received
        (ratio_1, ratio_2) = self.get_ratios(ratio)
        # Convert the two samples to integers
        intwave_sample_1 = np.fromstring(sample_1, np.int16)
        intwave_sample_2 = np.fromstring(sample_2, np.int16)
        # Mix the two samples together based on the calculated ratios
        intwave_mix = (intwave_sample_1 * ratio_1 + intwave_sample_2 * ratio_2).astype(np.int16)
        # Convert the new mix back to a playable bytestring
        mix = np.frombuffer(intwave_mix, np.byte)
        return mix

    def get_ratios(self, ratio: int):
        """
        Calculates the ratios using a received float

        :param ratio: A float betwenn 0 and 2 resembling the ratio between two things
        :return ratio_1, ratio_2: The two calculated actual ratios
        """

        ratio = float(ratio)
        ratio_1 = ratio / 2
        ratio_2 = (2 - ratio) / 2
        return ratio_1, ratio_2