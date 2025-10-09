# highlight_prioritiser.py
from typing import List, Dict, Optional


class HighlightPrioritiser:
    """
    Handles text prioritisation based on highlight metadata.
    Priorities:
        1: High priority — searched first.
        None: Non-highlighted text — searched after high.
        0: Low priority — searched last.
        -1: Excluded entirely.
    """

    def __init__(self, transcript: str, highlights: List[Dict]):
        self.transcript = transcript
        self.highlights = highlights
        self.priority_map = self._build_priority_segments()

    def _build_priority_segments(self):
        """Split transcript into segments tagged by highlight priority."""
        segments = []
        transcript_len = len(self.transcript)
        last_end = 0

        highlights_sorted = sorted(self.highlights, key=lambda h: h["start"])

        for h in highlights_sorted:
            start, end, priority = h["start"], h["end"], h["priority"]

            # Add non-highlighted text before this segment
            if start > last_end:
                segments.append({
                    "text": self.transcript[last_end:start],
                    "priority": None
                })

            # Add highlighted segment
            segments.append({
                "text": self.transcript[start:end],
                "priority": priority
            })
            last_end = end

        # Add trailing non-highlighted text
        if last_end < transcript_len:
            segments.append({
                "text": self.transcript[last_end:],
                "priority": None
            })

        return segments

    def get_best_answer(self, query: str) -> Optional[str]:
        """
        Simulate search across segments by priority order.
        Returns the first matching segment containing the query.
        """
        # Search order groups
        high_segments = [s for s in self.priority_map if s["priority"] and s["priority"] > 0]
        normal_segments = [s for s in self.priority_map if s["priority"] is None]
        low_segments = [s for s in self.priority_map if s["priority"] is not None and s["priority"] <= 0 and s["priority"] != -1]

        # Exclude -1
        all_groups = [("HIGH", high_segments), ("NORMAL", normal_segments), ("LOW", low_segments)]

        for label, group in all_groups:
            for seg in group:
                if query.lower() in seg["text"].lower():
                    return f"[{label}] → {seg['text'].strip()}"

        return "No relevant answer found (excluded or absent)."

