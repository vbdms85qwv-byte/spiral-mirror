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


# --- Pre-trigger loop interruption module ---

_OVERLOAD_CUES = (
    "overwhelmed",
    "too much",
    "flooded",
    "drowning",
    "can't handle",
    "can't cope",
    "burnt out",
    "exhausted",
    "frayed",
    "scattered",
)
_RUMINATION_CUES = (
    "can't stop thinking",
    "looping",
    "stuck",
    "spinning",
    "ruminating",
    "obsessing",
    "keeps replaying",
)
_HOPELESS_CUES = (
    "nothing will change",
    "no way out",
    "hopeless",
    "pointless",
    "never get better",
    "won't get better",
)
_NARROWING_CUES = (
    "everything feels",
    "all i can see",
    "all i see",
    "tunnel",
    "narrow",
    "can't see",
    "only thing",
)
_SELF_HARM_CUES = (
    "kill myself",
    "end it",
    "end my life",
    "suicide",
    "i want to die",
)

_REGULATION_CUES = {
    "overload": "For 60 seconds, exhale for 6 counts, then inhale for 4 counts.",
    "rumination": "For 45 seconds, name five objects you can see, one by one.",
    "hopeless": "For 60 seconds, press your feet into the floor and feel the contact.",
    "narrowing": "For 60 seconds, slowly widen your gaze to the edges of the room.",
    "default": "For 60 seconds, place a hand on your chest and feel the rise and fall.",
}

# --- Spiral Regulation Responses (pre-trigger, non-escalating) ---

_REGULATION_CUES.update({
    "overload": (
        "For 60 seconds, exhale slowly for 6 counts, then inhale for 4 counts. "
        "Let the exhale be longer than the inhale."
    ),
    "rumination": (
        "For 60 seconds, name five objects you can see, one by one, without judging them."
    ),
    "hopeless": (
        "For 60 seconds, press your feet gently into the floor and notice the contact."
    ),
    "narrowing": (
        "For 60 seconds, slowly widen your gaze to the edges of the room."
    ),
    "self-harm": (
        "This feeling is intense but temporary. For 60 seconds, place a hand on your chest and "
        "feel the rise and fall of your breath."
    ),
    "default": (
        "For 60 seconds, place a hand on your chest and feel the rise and fall of your breath."
    )
})

def pre_trigger_loop_interruption(text: str) -> str:
    """Return a single, calm response that reflects state and offers loop completion.

    This module is pre-emptive: it detects overload and narrowing cues to restore
    orientation without diagnosing or escalating the narrative.
    """
    cleaned = " ".join(text.strip().split())
    lowered = cleaned.casefold()

    # Detect overload/rumination/hopeless framing to mirror state, not story.
    signals = {
        "self_harm": _contains_any(lowered, _SELF_HARM_CUES),
        "overload": _contains_any(lowered, _OVERLOAD_CUES),
        "rumination": _contains_any(lowered, _RUMINATION_CUES),
        "hopeless": _contains_any(lowered, _HOPELESS_CUES),
        "narrowing": _contains_any(lowered, _NARROWING_CUES),
    }

    completion = _select_regulation_instruction(signals)

    if _has_any_signal(signals):
        reflection = _build_state_reflection(signals)
        closing = _graceful_exit(signals)
        if closing:
            return f"{reflection} {completion} {closing}"
        return f"{reflection} {completion}"

    return completion


def _contains_any(text: str, cues: tuple[str, ...]) -> bool:
    return any(cue in text for cue in cues)


def _build_state_reflection(signals: dict[str, bool]) -> str:
    # Mirror a single state to keep the response pre-narrative.
    if signals["self_harm"]:
        state = "in intense distress"
    elif signals["hopeless"]:
        state = "tilting toward hopeless framing"
    elif signals["overload"]:
        state = "overloaded"
    elif signals["rumination"]:
        state = "caught in a loop"
    elif signals["narrowing"]:
        state = "narrowing perception"
    else:
        state = "activated"

    return f"Your system is {state} right now."


def _has_any_signal(signals: dict[str, bool]) -> bool:
    return any(signals.values())


def _graceful_exit(signals: dict[str, bool]) -> str | None:
    if signals["self_harm"] or signals["hopeless"]:
        return "If you want, you could reach out to someone you trust."
    return None


def _select_regulation_instruction(signals: dict[str, bool]) -> str:
    # Offer a single, short loop-completion cue (30–90 seconds).
    if signals["self_harm"]:
        return _REGULATION_CUES["self-harm"]
    if signals["hopeless"]:
        return _REGULATION_CUES["hopeless"]
    if signals["overload"]:
        return _REGULATION_CUES["overload"]
    if signals["rumination"]:
        return _REGULATION_CUES["rumination"]
    if signals["narrowing"]:
        return _REGULATION_CUES["narrowing"]
    return _REGULATION_CUES["default"]
