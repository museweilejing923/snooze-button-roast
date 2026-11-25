"""Snooze Button Roast -- one-line entry writer.

The script owns one fixed sentence. It runs the sentence through
a list of rules first, and only writes it out when every rule
passes, so a broken entry can never reach the output file.
Nothing here reads input, touches the network, looks at the
clock, or rolls dice: the same sentence goes in, the same bytes
come out, every single run.
"""

import sys
from pathlib import Path

ENTRY = "Dear alarm clock: it is Saturday, 6 a.m., and the only emergency here is you. Even the birds are still asleep, and they have worms to catch."
LIMIT = 200
DEST = Path("/output/entry.txt")
END_MARKS = ".!?"


def _has_text(s):
    """True when the line holds more than blank space."""
    return bool(s and s.strip())


def _fits(s):
    """True when the line stays inside the bounty limit."""
    return len(s) <= LIMIT


def _no_controls(s):
    """True when no control character hides in the line."""
    return all(ord(ch) >= 32 and ord(ch) != 127 for ch in s)


def _tidy(s):
    """True when the edges are clean and the line stays on one line."""
    return (
        s == s.strip()
        and "  " not in s
        and "\n" not in s
        and "\r" not in s
        and "\t" not in s
    )


def _ends_with_mark(s):
    """True when the line closes with . ! or ?"""
    return bool(s) and s[-1] in END_MARKS


def _not_only_marks(s):
    """True when at least one letter or digit shows up."""
    return any(ch.isalnum() for ch in s)


def _not_only_digits(s):
    """True when the line is more than a bare number."""
    return not s.isdigit()


def _has_letters(s):
    """True when the line contains at least one letter."""
    return any(ch.isalpha() for ch in s)


def _on_topic(s):
    """True when the line roasts the alarm clock on a Saturday."""
    return "Saturday" in s and "alarm" in s.lower()


RULES = [
    (_fits, "entry is longer than the limit"),
    (_has_text, "entry is empty"),
    (_no_controls, "entry contains control characters"),
    (_tidy, "entry has ragged edges, double spaces, or line breaks"),
    (_ends_with_mark, "entry must end with . ! or ?"),
    (_not_only_marks, "entry is only punctuation"),
    (_not_only_digits, "entry is only digits"),
    (_has_letters, "entry has no letters"),
    (lambda s: "---" not in s, "entry contains a triple hyphen"),
    (_on_topic, "entry must mention Saturday and the alarm"),
]


def reject(reason):
    """Complain to stderr, then stop with a failing exit code."""
    print(f"rejected: {reason}", file=sys.stderr)
    raise SystemExit(1)


def check_entry(candidate):
    """Run the rule list; the first failing rule stops the run."""
    for test, reason in RULES:
        if not test(candidate):
            reject(reason)


def run():
    """Validate the fixed sentence, then write it out."""
    check_entry(ENTRY)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    run()
