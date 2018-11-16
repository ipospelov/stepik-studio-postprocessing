#!/usr/bin/env python3
import unittest

from stepik_studio_postprocessing.audio_processing.synchronization.cross_correlation_sync import CorrelationSynchronizer
from stepik_studio_postprocessing.utils import seconds_to_frames, AudioFileDescriptor


class TestCCSync(unittest.TestCase):
    def test_should_get_right_difference(self):
        fd_original = AudioFileDescriptor('data/test_non_delayed.wav')
        fd_delayed = AudioFileDescriptor('data/test_delayed.wav')

        real_diff = 0.5
        allowable_error = 0.005

        input_frequency = fd_original.get_framerate()
        self.assertTrue(input_frequency)

        chunksize = seconds_to_frames(3.0, input_frequency)

        synchronizer = CorrelationSynchronizer(chunksize=chunksize)

        computed_diff = synchronizer.get_seconds_diff(fd_original, fd_delayed)

        print(computed_diff)

        self.assertTrue(real_diff - allowable_error <= abs(computed_diff))
        self.assertTrue(real_diff + allowable_error >= abs(computed_diff))


