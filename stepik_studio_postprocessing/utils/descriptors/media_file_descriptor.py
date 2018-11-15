import os
import pathlib


class MediaFileDescriptor(object):
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError

        self.path = path
        self.suffix = pathlib.Path(path).suffix
