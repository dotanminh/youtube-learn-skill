import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "watch_video.py"
SPEC = importlib.util.spec_from_file_location("watch_video", MODULE_PATH)
watch_video = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(watch_video)


def response(data, status_code=200):
    result = Mock(status_code=status_code)
    result.json.return_value = {"code": "200", "data": data}
    result.raise_for_status.return_value = None
    return result


class AtlasProviderTests(unittest.TestCase):
    @patch.object(watch_video.time, "sleep")
    @patch.object(watch_video.requests, "get")
    @patch.object(watch_video.requests, "post")
    def test_uploads_submits_once_and_returns_transcript(self, post, get, _sleep):
        post.side_effect = [
            response({"download_url": "https://example.test/audio.mp3"}),
            response({"id": "prediction-1"}),
        ]
        get.return_value = response(
            {"status": "completed", "stt_result": {"text": "hello world"}}
        )

        with tempfile.NamedTemporaryFile(suffix=".mp3") as audio:
            transcript = watch_video.transcribe_audio_atlas(audio.name, "test-key")

        self.assertEqual(transcript, "hello world")
        self.assertEqual(post.call_count, 2)
        generation_call = post.call_args_list[1]
        self.assertEqual(
            generation_call.kwargs["json"]["model"], "bytedance/seed-asr-2.0"
        )
        self.assertEqual(generation_call.kwargs["json"]["format"], "mp3")

    @patch.object(watch_video.time, "sleep")
    @patch.object(watch_video.requests, "get")
    def test_prediction_get_retries_are_bounded(self, get, _sleep):
        get.side_effect = watch_video.requests.RequestException("temporary")

        with self.assertRaises(watch_video.requests.RequestException):
            watch_video.poll_atlas_transcription(
                "prediction-1", "test-key", max_polls=10, max_get_retries=2
            )

        self.assertEqual(get.call_count, 3)

    @patch.object(watch_video.time, "sleep")
    @patch.object(watch_video.requests, "get")
    def test_prediction_falls_back_to_outputs(self, get, _sleep):
        get.return_value = response({"status": "completed", "outputs": ["xin chao"]})

        transcript = watch_video.poll_atlas_transcription("prediction-1", "test-key")

        self.assertEqual(transcript, "xin chao")

    @patch.object(watch_video.time, "sleep")
    @patch.object(watch_video.requests, "get")
    def test_prediction_does_not_retry_non_transient_http_error(self, get, _sleep):
        bad_request = response({}, status_code=400)
        bad_request.raise_for_status.side_effect = watch_video.requests.HTTPError(
            "bad request"
        )
        get.return_value = bad_request

        with self.assertRaises(watch_video.requests.HTTPError):
            watch_video.poll_atlas_transcription("prediction-1", "test-key")

        self.assertEqual(get.call_count, 1)


if __name__ == "__main__":
    unittest.main()
