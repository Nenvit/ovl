import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ovl import loads, loadsarray, loadsiter
from ovl.utils.__internals import (
    BOOLEAN_TRANSLATION_MAP,
    BooleanParser,
)


class OVLTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()
        self.directory: Path = Path(self.temp_directory.name)

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def write_ovl(self, content: str, name: str = "settings.ovl") -> Path:
        path: Path = self.directory / name
        path.write_text(content, encoding="utf-8")
        return path


class PublicLoaderTests(OVLTestCase):
    def test_permissive_metadata_whitespace(self) -> None:
        path = self.write_ovl(
            "int]\tport $ networks .servers.server0 :\t8080\n"
        )

        result = loads(path, freeze=False)

        self.assertEqual(
            result["networks"]["servers"]["server0"]["port"],
            8080,
        )

    def test_newline_separated_value_with_whitespace(self) -> None:
        path = self.write_ovl(
            "int] port $ networks .servers.server0 :\n"
            "8080\n"
        )

        result = loads(path, freeze=False)

        self.assertEqual(
            result["networks"]["servers"]["server0"]["port"],
            8080,
        )

    def test_loads_returns_frozen_mapping_by_default(self) -> None:
        path = self.write_ovl("int] retries$network: 3\n")

        result = loads(path)

        self.assertEqual(result["network"]["retries"], 3)
        self.assertNotIsInstance(result, dict)

    def test_loads_can_return_mutable_mapping_and_apply_updates(self) -> None:
        path = self.write_ovl("int] retries$network: 3\n")

        result = loads(path, update={"environment": "test"}, freeze=False)
        if not isinstance(result, dict):
            self.fail("loads(freeze=False) should return a mutable dictionary")

        self.assertIsInstance(result, dict)
        self.assertEqual(result["environment"], "test")
        self.assertEqual(result["network"]["retries"], 3)
        result["environment"] = "changed"
        self.assertEqual(result["environment"], "changed")

    def test_loads_supports_nested_classes(self) -> None:
        path = self.write_ovl(
            "int] retries$network.timeout: 3\n"
            "text] name$application: OVL\n"
        )

        result = loads(path, freeze=False)

        self.assertEqual(result["network"]["timeout"]["retries"], 3)
        self.assertEqual(result["application"]["name"], "OVL")

    def test_loadsarray_preserves_file_order(self) -> None:
        path = self.write_ovl(
            "int] one: 1\n"
            "float] two: 2.5\n"
            "csv] three: red,green,blue\n"
        )

        result = loadsarray(path, freeze=False)

        self.assertIsInstance(result, list)
        self.assertEqual(result, [1, 2.5, ["red", "green", "blue"]])
        self.assertIsInstance(loadsarray(path), tuple)

    def test_loadsiter_can_return_values_or_keys(self) -> None:
        path = self.write_ovl("int] count$app: 4\nbool] active$app: yes\n")

        values = list(loadsiter(path, keys=False))
        keyed = list(loadsiter(path, keys=True))

        self.assertEqual(values, [4, True])
        self.assertEqual(keyed, [(b"app", b"count", 4), (b"app", b"active", True)])

    def test_nil_name_uses_automatic_numeric_index(self) -> None:
        path = self.write_ovl(
            "int] nil$items: 10\n"
            "int] nil$items: 20\n"
        )

        result = loads(path, freeze=False)

        self.assertEqual(result["items"][0], 10)
        self.assertEqual(result["items"][1], 20)

    def test_continuation_lines_are_ignored(self) -> None:
        path = self.write_ovl(
            "int] count$app: 2\n"
            "...ignored continuation\n"
            "text] name$app: OVL\n"
        )

        result = loads(path, freeze=False)

        self.assertEqual(result, {"app": {"count": 2, "name": "OVL"}})

    def test_supported_file_suffixes_are_accepted(self) -> None:
        for suffix in (".ovl", ".conf"):
            with self.subTest(suffix=suffix):
                path = self.write_ovl("int] count: 1\n", f"settings{suffix}")
                self.assertEqual(loads(path, freeze=False)["count"], 1)

    def test_missing_file_raises_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            loads(self.directory / "missing.ovl")

    def test_directory_path_raises_is_a_directory(self) -> None:
        with self.assertRaises(IsADirectoryError):
            loads(self.directory)

    def test_unsupported_suffix_raises_not_implemented(self) -> None:
        path = self.write_ovl("int] count: 1\n", "settings.txt")

        with self.assertRaises(NotImplementedError):
            loads(path)


class ConversionTests(OVLTestCase):
    def test_native_boolean_parser_true_false_and_unknown(self) -> None:
        self.assertIs(BooleanParser(b" YES "), True)
        self.assertIs(BooleanParser(b"false"), False)
        self.assertIs(BooleanParser(b"maybe"), None)

    def test_boolean_translation_maps_are_used(self) -> None:
        self.assertIn(b"yes", BOOLEAN_TRANSLATION_MAP.TRUE)
        self.assertIn(b"no", BOOLEAN_TRANSLATION_MAP.FALSE)

    def test_numeric_boolean_complex_and_blob_types(self) -> None:
        path = self.write_ovl(
            "int] integer: 42\n"
            "float] decimal: 2.5\n"
            "complex] complex: 1+2j\n"
            "blob] bytes: hello\n"
        )

        result = loads(path, freeze=False)

        self.assertEqual(result["integer"], 42)
        self.assertEqual(result["decimal"], 2.5)
        self.assertEqual(result["complex"], 1 + 2j)
        self.assertEqual(result["bytes"], b"hello")

    def test_delimited_and_json_types(self) -> None:
        path = self.write_ovl(
            "csv] csv: red, green, blue\n"
            "tsv] tsv: one\ttwo\tthree\n"
            "json] json: {\"enabled\": true}\n"
            "text] unknown: unchanged\n"
        )

        result = loads(path, freeze=False)

        self.assertEqual(result["csv"], ["red", "green", "blue"])
        self.assertEqual(result["tsv"], ["one", "two", "three"])
        self.assertEqual(result["json"], {"enabled": True})
        self.assertEqual(result["unknown"], "unchanged")

    def test_yaml_and_toml_types(self) -> None:
        path = self.write_ovl(
            "yaml] yaml: \n"
            "name: OVL\n"
            "items:\n"
            "  - one\n"
            "  - two\n"
            "toml] toml: \n"
            "[service]\n"
            "enabled=true\n"
        )

        result = loads(path, freeze=False)

        self.assertEqual(result["yaml"], {"name": "OVL", "items": ["one", "two"]})
        self.assertEqual(result["toml"], {"service": {"enabled": True}})

    def test_path_value_is_pathlib_path(self) -> None:
        path = self.write_ovl("path] location: ./data.ovl\n")

        result = loads(path, freeze=False)

        self.assertEqual(result["location"], Path("./data.ovl"))


if __name__ == "__main__":
    unittest.main()
