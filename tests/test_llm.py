import os
import unittest
from unittest import mock

from src.llm import generate_with_key, load_prompt, resolve_api_key


class LlmTests(unittest.TestCase):
    def test_empty_key_returns_none_without_client(self):
        with mock.patch("openai.OpenAI") as client:
            self.assertIsNone(generate_with_key("prompt", ""))
            client.assert_not_called()
        self.assertIsNone(generate_with_key("prompt", "   "))

    def test_client_error_returns_none(self):
        with mock.patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.side_effect = RuntimeError("boom")
            self.assertIsNone(generate_with_key("prompt", "sk-test", "gpt-4.1-mini"))

    def test_success_is_trimmed(self):
        with mock.patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.return_value.choices = [
                mock.Mock(message=mock.Mock(content="  draft  "))
            ]
            self.assertEqual(generate_with_key("prompt", "sk-test"), "draft")

    def test_empty_content_returns_none(self):
        with mock.patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.return_value.choices = [
                mock.Mock(message=mock.Mock(content=None))
            ]
            self.assertIsNone(generate_with_key("prompt", "sk-test"))

    def test_load_prompt(self):
        prompt = load_prompt("brd-generator")
        self.assertTrue(prompt.strip())
        self.assertEqual(load_prompt("does-not-exist"), "")

    def test_resolve_api_key(self):
        self.assertEqual(resolve_api_key("k"), "k")
        self.assertEqual(resolve_api_key("  "), "")

    def test_resolve_api_key_from_env(self):
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}, clear=False):
            self.assertEqual(resolve_api_key(None), "env-key")

    def test_resolve_api_key_missing(self):
        env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(resolve_api_key(None), "")


if __name__ == "__main__":
    unittest.main()
