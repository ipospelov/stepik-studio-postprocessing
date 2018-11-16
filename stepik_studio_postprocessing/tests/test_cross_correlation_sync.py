#!/usr/bin/env python3
import unittest

from stepik_studio_postprocessing.audio_processing.synchronization.cross_correlation_sync import CorrelationSynchronizer
from stepik_studio_postprocessing.utils import seconds_to_frames, AudioFileDescriptor


class TestCCSync(unittest.TestCase):
    def test_should_get_right_difference(self):
        fd_original = AudioFileDescriptor('data/source_1.wav')
        fd_delayed = AudioFileDescriptor('data/source_1_delayed_1_sec.wav')

        real_diff = 1.0
        allowable_error = 0.005

        input_frequency = fd_original.get_framerate()
        self.assertTrue(input_frequency)

        chunksize = seconds_to_frames(real_diff, input_frequency)
        synchronizer = CorrelationSynchronizer(chunksize=chunksize)

        computed_diff = synchronizer.get_seconds_diff(fd_original, fd_delayed)
        print(computed_diff)
        self.assertTrue(real_diff - allowable_error <= abs(computed_diff))
        self.assertTrue(real_diff + allowable_error >= abs(computed_diff))


