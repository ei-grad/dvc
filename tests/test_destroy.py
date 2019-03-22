import os

from mock import patch

from dvc.main import main

from tests.test_repro import TestRepro


class TestDestroyNoConfirmation(TestRepro):
    @patch("dvc.prompt.confirm", return_value=False)
    def test(self, mocked_confirm):
        ret = main(["destroy"])
        self.assertNotEqual(ret, 0)


class TestDestroyForce(TestRepro):
    def test(self):
        ret = main(["destroy", "-f"])
        self.assertEqual(ret, 0)

        self.assertFalse(os.path.exists(self.dvc.dvc_dir))
        self.assertFalse(os.path.exists(self.file1_stage))
        self.assertFalse(os.path.exists(self.file1))
