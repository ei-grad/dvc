from contextlib import contextmanager
import os

from mock import MagicMock, patch

import yaml

from dvc.scm import Git
from dvc.utils.compat import StringIO


def spy(method_to_decorate):
    mock = MagicMock()

    def wrapper(self, *args, **kwargs):
        mock(*args, **kwargs)
        return method_to_decorate(self, *args, **kwargs)

    wrapper.mock = mock
    return wrapper


def get_gitignore_content():
    with open(Git.GITIGNORE, "r") as gitignore:
        return gitignore.read().splitlines()


def load_stage_file(path):
    with open(path, "r") as fobj:
        return yaml.safe_load(fobj)


def reset_logger_error_output():
    from dvc.logger import logger

    logger.handlers[1].stream = StringIO()


def reset_logger_standard_output():
    from dvc.logger import logger

    logger.handlers[0].stream = StringIO()


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


class MockIsatty(object):

    isatty_ret_value = False

    def setUp(self):
        super(MockIsatty, self).setUp()
        self.isatty_patch = patch(
            "sys.stdout.isatty", return_value=self.isatty_ret_value
        )
        self.isatty_mock = self.isatty_patch.start()

    def tearDown(self):
        self.isatty_patch.stop()
        super(MockIsatty, self).tearDown()
