#!/usr/bin/env bash
# Install neospark-cli from source via pip.
# Works on macOS and Linux. Requires Python 3.8+ and pip.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

PYTHON_CMD="${PYTHON_CMD:-python3}"

if ! command -v "${PYTHON_CMD}" >/dev/null 2>&1; then
    echo "Error: ${PYTHON_CMD} not found. Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$("${PYTHON_CMD}" -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
MIN_VERSION="3.8"

if [ "$(printf '%s\n' "${MIN_VERSION}" "${PYTHON_VERSION}" | sort -V | head -n1)" != "${MIN_VERSION}" ]; then
    echo "Error: Python ${PYTHON_VERSION} is too old. Requires Python ${MIN_VERSION}+."
    exit 1
fi

echo "Installing neospark-cli from ${PROJECT_ROOT} (Python ${PYTHON_VERSION})..."
"${PYTHON_CMD}" -m pip install --upgrade pip
"${PYTHON_CMD}" -m pip install "${PROJECT_ROOT}"

echo ""
echo "Installed. Verify with: neospark --version"
