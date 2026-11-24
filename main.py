#!/usr/bin/env python3
"""Everyday Things, Two Lines — entry program.

Writes the two-line explanation to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure stdlib only.

Line 1 explains a queue to a 10-year-old in one vivid sentence built on
a single analogy (a slow caterpillar made of people). Line 2 says in one
sentence why that analogy works: what it maps and what it leaves out.
"""

import os
import sys

LINE_1 = (
    "A queue is a slow caterpillar made of people, shuffling forward "
    "one tiny step at a time until its head reaches the front."
)
LINE_2 = (
    "It maps how everyone moves in one line and waits their turn, but "
    "it leaves out that real caterpillars never get bored, push ahead, "
    "or need a ticket when they arrive."
)
# The second line names three concrete limits on purpose: a caterpillar
# never feels bored (a queue does, to the people in it), never cuts in
# line, and never pays at the front — each one is a place where the
# analogy stops, stated plainly instead of praising the comparison.

ENTRY = LINE_1 + "\n" + LINE_2


def gate(text):
    """Self-check the entry against the competition gate before writing."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not text.strip():
        raise ValueError("entry is only white space")
    if not (1 <= len(text) <= 400):
        raise ValueError("entry must be 1 to 400 characters, got %d" % len(text))
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two lines, got %d" % len(lines))
    for i, line in enumerate(lines, 1):
        if line != line.strip():
            raise ValueError("line %d has leading or trailing whitespace" % i)
        if not line:
            raise ValueError("line %d is empty" % i)
        if line.count(".") != 1 or not line.endswith("."):
            raise ValueError("line %d must be exactly one sentence" % i)
        if any(ord(ch) < 32 and ch != "\n" for ch in line):
            raise ValueError("line %d holds a control character" % i)
        if "  " in line:
            raise ValueError("line %d holds doubled spaces" % i)
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = gate(ENTRY)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read back and verify byte-identical, so a partial write never slips by.
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise ValueError("read-back mismatch in entry.txt")
    os.chmod(path, 0o644)
    print("wrote %s (%d characters, 2 lines)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
