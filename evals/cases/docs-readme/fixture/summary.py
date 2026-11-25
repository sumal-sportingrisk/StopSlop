"""Offline summary CLI. Run with Python 3 and no additional dependencies."""

import argparse
import json
from pathlib import Path


def summarize(path):
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return {"count": len(rows)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    print(json.dumps(summarize(parser.parse_args().path)))
