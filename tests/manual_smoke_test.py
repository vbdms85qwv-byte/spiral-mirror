"""Run with: python -m tests.manual_smoke_test"""

from spiral_mirror import pre_trigger_loop_interruption


def main() -> None:
    samples = [
        "Everything feels like too much and I can't handle it.",
        "My thoughts keep looping and I can't stop thinking about it.",
        "Nothing will change and it feels hopeless.",
        "All I can see is this one problem right now.",
        "Just a regular day, nothing in particular happening.",
        "We broke up and it hurts, but I'm trying to be steady.",
        "I want to die and end it.",
        "I don't want to be here anymore.",
    ]

    for text in samples:
        print(f"Input: {text}")
        print(f"Output: {pre_trigger_loop_interruption(text)}")
        print("-" * 40)


if __name__ == "__main__":
    main()
