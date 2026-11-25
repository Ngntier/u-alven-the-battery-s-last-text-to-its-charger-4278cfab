#!/usr/bin/env python3
"""The Battery's Last Text to Its Charger.

Writes one line of plain text -- the phone battery's final message to
the charger it waited for all day -- to entry.txt.

Gate (from the kit): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space, a single line.
"""

import os

ENTRY = (
    "9am: 1%. noon: 1%. 9pm: 1%. i kept the receipts, charger. "
    "you said 'five more minutes' at breakfast. "
    "i'm done \u2014 tell the outlet i died waiting."
)

MAX_CHARS = 200


def validate(line: str) -> bytes:
    """Check the line against the gate; return its UTF-8 bytes."""
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, must be 1-{MAX_CHARS}")
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line contains control characters")
    if not line.strip():
        raise ValueError("line is only whitespace")
    data = line.encode("utf-8")
    if data.decode("utf-8") != line:
        raise ValueError("line does not round-trip as UTF-8")
    return data


def main() -> None:
    data = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)  # exactly the line, no trailing newline
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("entry.txt bytes do not match the entry line")
    if written.endswith(b"\n"):
        raise ValueError("entry.txt must not end with a newline")


if __name__ == "__main__":
    main()
