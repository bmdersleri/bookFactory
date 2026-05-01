# -*- coding: utf-8 -*-
"""Module entry point for `python -m bookfactory`."""
from __future__ import annotations

import os
import sys

from .cli import main


if __name__ == "__main__":
    try:
        code = int(main())
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 0
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(int(code))
