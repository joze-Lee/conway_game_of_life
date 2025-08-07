# gpt_tool/gpt_tool.py

import random
from conway_api.conway import run_until_stable

class ConwayGPTTool:
    """
    A tool to interface Conway simulation with LLM-like prompts.
    """

    def __init__(self):
        pass

    def simulate_word(self, word: str) -> dict:
        """
        Given a word, return generations until stability and score.
        """
        return run_until_stable(word)

    def generate_random_words(self, count=3) -> list[str]:
        """
        Generate random English words for testing.
        (Simple static list for demo; extend with real random word generation if needed)
        """
        sample_words = [
            "monument", "castle", "river", "forest", "python", "challenge",
            "conway", "matrix", "alpha", "beta", "gamma", "delta"
        ]
        return random.sample(sample_words, count)

    def highest_score_among_random_words(self, count=3) -> dict:
        """
        Generates random words, runs Conway simulation on each, and returns the
        word with the highest Conway score.
        """
        words = self.generate_random_words(count)
        results = {w: run_until_stable(w) for w in words}
        highest_word = max(results, key=lambda w: results[w]["score"])
        return {
            "words": words,
            "highest_word": highest_word,
            "highest_score": results[highest_word]["score"],
            "result": results[highest_word]
        }
