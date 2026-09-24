#!/usr/bin/env bash
# Build a platform-independent wheel for neospark-cli.
# Works on macOS and Linux. Requires Python 3.8+ and pip.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

PYTHON_CMD="${PYTHON_CMD:-python3}"

if ! command -v "${PYTHON_CMD}" >/dev/null 2>&1; then
    echo "Error: ${PYTHON_CMD} not found. Please install Python 3.8 or later."
    exit 1
fi

"${PYTHON_CMD}" -m pip install --upgrade pip build
"${PYTHON_CMD}" -m build --wheel "${PROJECT_ROOT}"

echo ""
echo "Wheel built: ${PROJECT_ROOT}/dist/"
ls -l "${PROJECT_ROOT}/dist"
