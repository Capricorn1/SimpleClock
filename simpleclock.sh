#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Require Python 3
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3 to run this app." >&2
    exit 1
fi

# Require tkinter (stdlib but needs OS package on some distros, e.g. python3-tk)
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "ERROR: Python module 'tkinter' is not available." >&2
    echo "  On Debian/Ubuntu:  sudo apt install python3-tk" >&2
    echo "  On Fedora/RHEL:    sudo dnf install python3-tkinter" >&2
    echo "  On Arch:           sudo pacman -S tk" >&2
    exit 1
fi

# datetime is always present in Python 3, but verify anyway
if ! python3 -c "import datetime" 2>/dev/null; then
    echo "ERROR: Python module 'datetime' is not available. Check your Python installation." >&2
    exit 1
fi

python3 "$SCRIPT_DIR/clock.py" &
echo "SimpleClock started (PID $!)"
