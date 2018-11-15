import contextlib
import wave

from stepik_studio_postprocessing.utils.descriptors.media_file_descriptor import MediaFileDescriptor
from stepik_studio_postprocessing.utils.types.audio_suffixes import AudioSuffixes
from stepik_studio_postprocessing.utils.types.media_types import MediaTypes


class AudioFileDescriptor(MediaFileDescriptor):
    def __init__(self, path: str):
        super().__init__(path)

        if AudioSuffixes.has_value(self.suffix):
            self.media_type = MediaTypes.AUDIO
            self.audio_type = AudioSuffixes(self.suffix)
        else:
            raise TypeError('Audio descriptor doesn\'t support {} files'.format(self.suffix))

    def get_framerate(self):
        with contextlib.closing(wave.open(self.path, 'r')) as f:
            framerate = f.getframerate()

        return framerate