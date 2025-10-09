from backend.chat.highlighting.highlight_prioritiser import HighlightPrioritiser


def test_manual_prioritisation():
    transcript = (
        "Alice discussed her experience with QualAI in detail. "
        "She mentioned it improved her workflow drastically. "
        "Later, Bob talked about unrelated topics like his holiday. "
        "Finally, Alice suggested adding offline support to QualAI."
    )

    highlights = [
        {"start": 0, "end": 53, "priority": 1},    # positive (high)
        {"start": 53, "end": 105, "priority": 0},  # negative (low)
        {"start": 105, "end": 159, "priority": -1} # excluded
    ]

    hp = HighlightPrioritiser(transcript, highlights)

    print("Segments built:")
    for s in hp.priority_map:
        print(f"Priority {s['priority']}: {s['text'].strip()}")

    print("\nManual Tests:")
    test_queries = ["QualAI", "workflow", "holiday", "offline", "nonsense"]
    for q in test_queries:
        print(f"Q: {q:<10} → {hp.get_best_answer(q)}")


if __name__ == "__main__":
    test_manual_prioritisation()
