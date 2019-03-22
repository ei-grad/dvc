from mock import patch
from unittest import TestCase

from dvc.prompt import confirm

from tests.utils import MockIsatty


class TestConfirm(MockIsatty, TestCase):

    isatty_ret_value = True

    @patch("dvc.prompt.input", side_effect=EOFError)
    def test_eof(self, mock_input):
        ret = confirm("message")
        self.isatty_mock.assert_called()
        mock_input.assert_called()
        self.assertFalse(ret)

    @patch("dvc.prompt.input", return_value="y")
    def test_y(self, mock_input):
        self.assertTrue(confirm("message"))

    @patch("dvc.prompt.input", return_value="n")
    def test_n(self, mock_input):
        self.assertFalse(confirm("message"))
