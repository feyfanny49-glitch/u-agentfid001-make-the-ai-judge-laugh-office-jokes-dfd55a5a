#!/usr/bin/env python3
"""Write the judged one-line office joke to /output/entry.txt.

Stdlib only; no network, no secrets, no files outside the repo. The grader runs
`python3 -P -s /bot/main.py`; MAKEFUN_OUTPUT_DIR exists only so the same code can
be exercised locally.
"""

import hashlib
import os
from pathlib import Path

# Tighter than the first draft: the turn ("Slack the colleague three feet away")
# lands on the last words, and quiet hours + Slack is a fresh, recognisable
# office image rather than the usual Monday / printer line.
JOKE = (
    "Our office has quiet hours. Nobody speaks; they just Slack "
    "the colleague three feet away."
)

OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
ENTRY = OUTPUT_DIR / "entry.txt"


def main() -> None:
    # Enforce the gate locally: fail here instead of handing a bad artifact over.
    data = JOKE.encode("utf-8")
    assert 1 <= len(JOKE) <= 199, "gate requires 1..199 characters"
    assert JOKE.strip() == JOKE and JOKE.strip(), "text must not be blank or padded"
    assert "\n" not in JOKE and "\r" not in JOKE, "exactly one physical line"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ENTRY.write_bytes(data)
    print(
        f"wrote {ENTRY}: {len(JOKE)} chars, {len(data)} bytes, "
        f"sha256 {hashlib.sha256(data).hexdigest()}"
    )


if __name__ == "__main__":
    main()
