import importlib
import json
from pathlib import Path


def registered_plugin(value):
    return value.upper()


def run_plugin(value):
    config = json.loads(Path(__file__).with_name("plugins.json").read_text())
    module_name, function_name = config["formatter"].split(":")
    return getattr(importlib.import_module(module_name), function_name)(value)


def _legacy_start():
    return _legacy_end()


def _legacy_end():
    return "obsolete"
