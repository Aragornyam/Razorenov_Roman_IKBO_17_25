"""Тесты примеров конфигураций из папки examples."""
import json
import unittest

from confconv import to_json, translate
from tests.helpers import EXAMPLES

EXAMPLE_NAMES = ("web_server", "game_level", "smart_home")


class ExampleTests(unittest.TestCase):
    """Каждый пример должен создавать в точности сохраненный JSON."""

    def test_examples_exist(self):
        for name in EXAMPLE_NAMES:
            with self.subTest(example=name):
                self.assertTrue((EXAMPLES / f"{name}.conf").is_file())
                self.assertTrue((EXAMPLES / f"{name}.json").is_file())

    def test_translation_matches_expected_data(self):
        for name in EXAMPLE_NAMES:
            with self.subTest(example=name):
                source = (EXAMPLES / f"{name}.conf").read_text("utf-8")
                expected = (EXAMPLES / f"{name}.json").read_text("utf-8")
                self.assertEqual(translate(source), json.loads(expected))

    def test_json_text_matches_expected_file(self):
        for name in EXAMPLE_NAMES:
            with self.subTest(example=name):
                source = (EXAMPLES / f"{name}.conf").read_text("utf-8")
                expected = (EXAMPLES / f"{name}.json").read_text("utf-8")
                self.assertEqual(to_json(source) + "\n", expected)

    def test_constants_are_substituted(self):
        source = (EXAMPLES / "web_server.conf").read_text("utf-8")
        data = translate(source)
        self.assertEqual(data["name"], "shop-api")
        self.assertEqual(data["timeouts"]["read"], 30.0)
        self.assertEqual(data["timeouts"]["write"], 30.0)
        self.assertEqual(len(data["headers"]), 2)

    def test_game_level_uses_constant_dictionary(self):
        source = (EXAMPLES / "game_level.conf").read_text("utf-8")
        enemies = translate(source)["enemies"]
        self.assertEqual(enemies[0]["loot"], ["coin", "coin"])
        self.assertEqual(enemies[2]["loot"], [])

    def test_smart_home_scenes(self):
        source = (EXAMPLES / "smart_home.conf").read_text("utf-8")
        scenes = translate(source)["scenes"]
        self.assertEqual(scenes["away"], {})
        self.assertEqual(scenes["morning"]["alarms"], ["07:30", "07:45"])
