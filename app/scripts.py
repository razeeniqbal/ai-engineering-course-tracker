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


# --- loading prepared scripts from course/scripts/*.md ----------------------------

_SECTION_RE = re.compile(r"^## (E\d{3}) · [CB] · .*$", re.MULTILINE)


def read_script_files(directory) -> dict[str, str]:
    """{episode code: script markdown} from files whose episodes are headed '## E012 · B · Title'."""
    from pathlib import Path

    found: dict[str, str] = {}
    for path in sorted(Path(directory).glob("*.md")):
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        parts = _SECTION_RE.split(text)
        for i in range(1, len(parts), 2):
            code, body = parts[i], parts[i + 1].strip()
            if code in found:
                raise ValueError(f"{code} appears twice in {directory}")
            found[code] = body
    return found


@dataclass
class LoadResult:
    filled: list[str]
    skipped: list[str]  # already had a script and overwrite was off
    unknown: list[str]  # codes not in the active course version


def load_scripts(db, scripts: dict[str, str], overwrite: bool = False) -> LoadResult:
    from sqlalchemy import select

    from app.importer import active_version
    from app.models import EpisodeProgress

    version = active_version(db)
    if version is None:
        raise ValueError("No course is loaded yet.")
    keys = dict(db.execute(select(Episode.code, Episode.episode_key).where(Episode.version_id == version.id)).all())
    result = LoadResult([], [], [])
    for code, markdown in sorted(scripts.items()):
        if code not in keys:
            result.unknown.append(code)
            continue
        progress = db.get(EpisodeProgress, keys[code])
        if progress.script_markdown and not overwrite:
            result.skipped.append(code)
            continue
        progress.script_markdown = markdown[:MAX_SCRIPT_CHARS]
        result.filled.append(code)
    db.commit()
    return result
