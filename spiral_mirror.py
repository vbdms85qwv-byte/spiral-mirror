"""Spiral Mirror: non-diagnostic nervous system reflection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MirrorResult:
    pattern: str
    reflection: str
    grounding: str | None


_PATTERN_RULES: tuple[tuple[str, tuple[str, ...], str | None], ...] = (
    (
        "anxious activation",
        (
            "anxious",
            "anxiety",
            "worried",
            "worry",
            "panic",
            "panicky",
            "tight",
            "racing",
            "can't settle",
        ),
        "If you'd like, try a slow exhale longer than the inhale.",
    ),
    (
        "shutdown or numbness",
        ("numb", "blank", "shut down", "frozen", "flat", "disconnected"),
        "If you'd like, notice three things you can see in the room.",
    ),
    (
        "overwhelm",
        ("overwhelmed", "too much", "can't handle", "flooded", "drowning"),
        "If you'd like, feel your feet on the floor for a moment.",
    ),
    (
        "sadness or heaviness",
        ("sad", "heavy", "grief", "down", "tearful", "cry"),
        None,
    ),
    (
        "anger or heat",
        ("angry", "mad", "furious", "rage", "irritated"),
        None,
    ),
)


def mirror(text: str) -> dict[str, str | None]:
    """Mirror user language into pattern, reflection, and optional grounding cue.

    Args:
        text: One paragraph of user text.

    Returns:
        A dictionary with keys: pattern, reflection, grounding.
    """
    cleaned = " ".join(text.strip().split())
    snippet = _trim_to_words(cleaned, max_words=22)
    pattern, grounding = _classify_pattern(cleaned)
    reflection = f"Noticing: {snippet}." if snippet else "Noticing:"
    return {
        "pattern": pattern,
        "reflection": reflection,
        "grounding": grounding,
    }


def _classify_pattern(text: str) -> tuple[str, str | None]:
    lowered = text.casefold()
    for pattern, keywords, grounding in _PATTERN_RULES:
        if any(keyword in lowered for keyword in keywords):
            return pattern, grounding
    return "neutral observation", None


def _trim_to_words(text: str, max_words: int) -> str:
    words = text.split()
    if not words:
        return ""
    trimmed = words[:max_words]
    return " ".join(trimmed)
