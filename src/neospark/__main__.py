"""Allow running as `python -m neospark`."""
from __future__ import annotations

import sys

from neospark.cli import main

if __name__ == "__main__":
    sys.exit(main())
