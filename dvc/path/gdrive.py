from dvc.scheme import Schemes
from .base import PathBASE


class PathGDrive(PathBASE):
    """Google Drive resource path information

    Args:
        root: the reference folder ID, root node or
            regular folder
        path: a posix-like file path relative to `root`

    """

    scheme = Schemes.GDRIVE

    def __init__(self, root, url=None, path=None):
        super(PathGDrive, self).__init__(url, path)
        self.root = root
