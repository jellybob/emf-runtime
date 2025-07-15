import unittest
from unittest.mock import patch

from summarize_youtube import (
    format_duration,
    get_all_video_ids,
    get_total_duration,
    render_html,
)


class TestSummarizeYouTube(unittest.TestCase):
    def test_format_duration(self):
        # 1 day, 2 hours, 3 minutes = 93780 seconds
        days, hours, minutes = format_duration(93780)
        self.assertEqual((days, hours, minutes), (1, 2, 3))

    def test_render_html(self):
        html = render_html(1, 2, 3, 93780, 42)
        self.assertIn("1 days", html)
        self.assertIn("2 hours", html)
        self.assertIn("3 minutes", html)
        self.assertIn("93780 seconds", html)
        self.assertIn("42 videos", html)

    @patch("summarize_youtube.requests.get")
    def test_get_all_video_ids(self, mock_get):
        # Simulate two pages of results
        mock_get.side_effect = [
            # First page
            unittest.mock.Mock(
                **{
                    "json.return_value": {
                        "items": [
                            {"id": {"videoId": "vid1"}},
                            {"id": {"videoId": "vid2"}},
                        ],
                        "nextPageToken": "NEXT",
                    }
                }
            ),
            # Second page
            unittest.mock.Mock(
                **{"json.return_value": {"items": [{"id": {"videoId": "vid3"}}]}}
            ),
        ]
        vids = get_all_video_ids("fakekey", "fakechan")
        self.assertEqual(vids, ["vid1", "vid2", "vid3"])

    @patch("summarize_youtube.requests.get")
    def test_get_total_duration(self, mock_get):
        # Simulate a single batch of 2 videos
        mock_get.return_value.json.return_value = {
            "items": [
                {"contentDetails": {"duration": "PT1H2M3S"}},
                {"contentDetails": {"duration": "PT4M5S"}},
            ]
        }
        # Patch parse_iso8601_duration to avoid dependency on isodate
        with patch("summarize_youtube.parse_iso8601_duration") as mock_parse:
            mock_parse.side_effect = [3723, 245]  # 1:02:03 and 4:05 in seconds
            total = get_total_duration("fakekey", ["v1", "v2"])
            self.assertEqual(total, 3723 + 245)


if __name__ == "__main__":
    unittest.main()
