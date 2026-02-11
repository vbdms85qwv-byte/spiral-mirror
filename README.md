# Spiral Mirror

Spiral Mirror is a **non-diagnostic nervous system reflection tool**. It mirrors a single paragraph of user language into:

- a named emotional or nervous-system pattern
- a brief reflection sentence
- one optional grounding cue (breath or orientation)

It does **not** give advice, explain psychology, diagnose, coach, persuade, or reframe positively.

## Usage

```python
from spiral_mirror import mirror

text = "I can't settle down and my chest feels tight; I'm worried about everything."
result = mirror(text)
print(result)
```

Example output:

```python
{
  "pattern": "anxious activation",
  "reflection": "Noticing: I can't settle down and my chest feels tight; I'm worried about everything.",
  "grounding": "If you'd like, try a slow exhale longer than the inhale."
}
```

## Input / Output

- **Input:** one paragraph of user text (string)
- **Output:** a short structured reflection (`pattern`, `reflection`, `grounding`)

## Additional framework notes

- `STOP_THE_LOOP_CODEX.md` contains the full "Irradiated Lens Framework" outline (Version 1.0), including mechanisms, detection protocols, regulation methods, application scenarios, and messaging templates.
