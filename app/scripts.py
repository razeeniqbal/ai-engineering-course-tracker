"""Episode scripts: the two-minute outline from the course, and spoken-word counts.

The course's script format (Section 9) puts spoken lines in blockquotes ("> ...") and screen
directions in italics, so when a script has blockquotes only those lines are counted.
"""

import re
from dataclasses import dataclass

from app.models import Episode

MAX_SCRIPT_CHARS = 50_000
WORDS_PER_MINUTE = 130  # 260 spoken words ≈ 2:00, the top of the course's 220–260 target
TARGET = {"C": (220, 260), "B": (180, 240)}  # Build episodes use fewer words so viewers can read the screen

_WORD_RE = re.compile(r"[\w'’-]+")


@dataclass
class ScriptStats:
    words: int
    seconds: int
    low: int
    high: int
    spoken_only: bool

    @property
    def verdict(self) -> str:
        if self.words == 0:
            return "empty"
        if self.words < self.low:
            return "short"
        return "over" if self.words > self.high else "on-target"

    @property
    def duration(self) -> str:
        return f"{self.seconds // 60}:{self.seconds % 60:02d}"


def spoken_text(markdown: str) -> tuple[str, bool]:
    lines = markdown.splitlines()
    quoted = [ln.lstrip()[1:] for ln in lines if ln.lstrip().startswith(">")]
    return ("\n".join(quoted), True) if quoted else (markdown, False)


def stats(markdown: str | None, episode_type: str) -> ScriptStats:
    text, spoken_only = spoken_text(markdown or "")
    words = len(_WORD_RE.findall(text))
    low, high = TARGET.get(episode_type, TARGET["C"])
    return ScriptStats(words, round(words * 60 / WORDS_PER_MINUTE), low, high, spoken_only)


def outline(episode: Episode, next_episode: Episode | None) -> str:
    """A starting script in the course's two-minute format, seeded from the episode spec."""
    next_line = f" Next: {next_episode.title}." if next_episode else ""
    return (
        "**0:00–0:15 · Hook**\n"
        "*Screen: *\n"
        f"> {episode.hook}\n\n"
        "**0:15–0:45 · Claim**\n"
        "*Screen: *\n"
        f"> {episode.claim}\n\n"
        "**0:45–1:30 · Show**\n"
        f"*Screen: {episode.show}*\n"
        "> \n\n"
        "**1:30–1:50 · Gotcha**\n"
        "*Screen: *\n"
        f"> {episode.gotcha}\n\n"
        "**1:50–2:00 · Takeaway**\n"
        f"*Screen: \"{episode.takeaway}\"*\n"
        f"> {episode.takeaway}{next_line}\n"
    )
