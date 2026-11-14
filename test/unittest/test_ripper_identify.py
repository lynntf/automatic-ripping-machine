import unittest
from types import SimpleNamespace
from unittest.mock import patch

from arm.ripper import utils
from arm.ripper.identify import apply_disc_type_override


class TestDiscTypeOverride(unittest.TestCase):
    def test_auto_preserves_detected_type(self):
        job = SimpleNamespace(disctype="bluray")

        apply_disc_type_override(job, "auto")

        self.assertEqual(job.disctype, "bluray")

    def test_override_selects_pipeline_type(self):
        expected_types = {
            "dvd": "dvd",
            "bluray": "bluray",
            "music": "music",
            "data": "data",
        }

        for override, expected_type in expected_types.items():
            with self.subTest(override=override):
                job = SimpleNamespace(disctype="unknown")
                with patch("arm.ripper.identify.music_brainz.main", return_value="Album") as music_brainz:
                    apply_disc_type_override(job, override)

                self.assertEqual(job.disctype, expected_type)
                if override == "music":
                    self.assertEqual(job.label, "Album")
                    music_brainz.assert_called_once_with(job)
                else:
                    music_brainz.assert_not_called()

    def test_invalid_override_is_rejected(self):
        with self.assertRaises(utils.RipperException):
            apply_disc_type_override(SimpleNamespace(disctype="dvd"), "video")


if __name__ == "__main__":
    unittest.main()
