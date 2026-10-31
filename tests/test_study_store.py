import unittest
from unittest.mock import Mock, patch

import study_store


class PaidFileDeliveryTests(unittest.TestCase):
    def test_downloads_only_the_two_expected_private_pdfs(self):
        listing = Mock(ok=True)
        listing.json.return_value = {
            "files": [
                {"id": "paper-id", "name": "questionpaper2020", "mimeType": "application/pdf"},
                {"id": "notes-id", "name": "physics.unit 1 and 2.pdf", "mimeType": "application/pdf"},
                {"id": "extra-id", "name": "unrelated.pdf", "mimeType": "application/pdf"},
            ]
        }
        notes = Mock(ok=True, content=b"notes")
        paper = Mock(ok=True, content=b"paper")
        session = Mock()
        session.get.side_effect = [listing, notes, paper]

        with (
            patch.object(study_store, "_drive_session", return_value=session),
            patch.object(study_store.st, "secrets", {"drive": {"folder_id": "folder-id"}}),
        ):
            downloads = study_store.load_paid_files()

        self.assertEqual(
            downloads,
            [("physics.unit 1 and 2.pdf", b"notes"), ("questionpaper2020.pdf", b"paper")],
        )
        self.assertEqual(session.get.call_count, 3)

    def test_missing_expected_file_is_an_error(self):
        listing = Mock(ok=True)
        listing.json.return_value = {
            "files": [{"id": "notes-id", "name": "physics.unit 1 and 2", "mimeType": "application/pdf"}]
        }
        session = Mock()
        session.get.return_value = listing

        with (
            patch.object(study_store, "_drive_session", return_value=session),
            patch.object(study_store.st, "secrets", {"drive": {"folder_id": "folder-id"}}),
            self.assertRaises(study_store.DeliveryError),
        ):
            study_store.load_paid_files()

        self.assertEqual(session.get.call_count, 1)


if __name__ == "__main__":
    unittest.main()
