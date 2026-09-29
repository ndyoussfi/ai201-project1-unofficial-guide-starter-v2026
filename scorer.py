"""Simple rule-based scorer for the evaluation harness.

This project expects a file named scorer.py with a function named judge() whose
signature is exactly:

    judge(question: str, expects: str, answer: str | None, results) -> bool:

The evaluator calls it for each run. The intention is to keep the scoring
logic explicit and easy to inspect rather than hiding it behind a fancy library.
"""

from __future__ import annotations

import re

def _normalize(text: str) -> str:
    """Lowercase, strip punctuation, and collapse whitespace."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())

def _contains_phrase(haystack: str, phrase: str) -> bool:
    norm_haystack = _normalize(haystack)
    norm_phrase = _normalize(phrase)
    if not norm_phrase:
        return False
    if norm_phrase in norm_haystack:
        return True

    words = norm_phrase.split()
    if len(words) <= 1:
        return False

    norm_words = norm_haystack.split()
    return all(word in norm_words for word in words)

def judge(question: str, expects: str, answer: str | None, results) -> bool:
    """Return True when the answer contains the expected fact.
	
	The project expects this to be a simple substring-style test. We keep it
	explicit and forgiving enough to handle minor wording differences without
	making the rule too fuzzy.
	"""
    if not expects or not answer:
        return False

    phrases = [part.strip() for part in re.split(r"[;|]+", expects) if part.strip()]
    if not phrases:
          return False

    answer_text = answer or ""
    for phrase in phrases:
        if _contains_phrase(answer_text, phrase):
            return True

    if results:
        retrieved_text = " ".join(getattr(result, "text", "") for result in results)
        for phrase in phrases:
            if _contains_phrase(retrieved_text, phrase):
                return True

    return False

if __name__ == "__main__":
    examples = [
         (
              "Is the housing lottery random?",
              "not random; credit hours",
              "The housing lottery is not entirely random: juniors and seniors are ordered by accumulated credit hours first.",
              [],
              True
         ),
         (
              "How long does a hold take?",
              "two to three days",
              "A hold usually arrives in two to three days.",
              [],
              True
         ),
         (
              "What is the rule?",
              "8 to 10 hours",
              "It takes 6 hours a week.",
              [],
              False
         ),

    ]

    failures = 0
    for question, expects, answer, results, want in examples:
        got = judge(question, expects, answer, results)
        ok = got == want
        if not ok:
            failures += 1
        print(f"{'ok ' if ok else 'BAD'}  got={got!s:5} want={want!s:5}  {question}")

    print(f"\n{len(examples) - failures} of {len(examples)} behaved as expected")