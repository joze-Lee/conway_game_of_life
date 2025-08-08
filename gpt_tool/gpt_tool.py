# gpt_tool/gpt_tool.py
import random
import re
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

    def handle_prompt(self, prompt: str) -> str:
        try:
            if "How many generations" in prompt and "word" in prompt:
                # word = prompt.split("word")[-1].split(" ")[0].strip(" ‘'?\".")
                match = re.search(r"[‘']([^’']+)[’']", prompt)
                if match:
                    word = match.group(1)
                    print(word)  # Output: monument
                else:
                    return "No word found"
                result = self.simulate_word(word)
                return f"The word '{word}' returns {result['generations']} generations and a score of {result['score']}."
            print(prompt.split())
            if "Generate 3 random words" in prompt and "highest Conway score" in prompt:
                result = self.highest_score_among_random_words(3)
                return (f"Generated words: {', '.join(result['words'])}. "
                        f"Highest Conway score is from '{result['highest_word']}' with a score of {result['highest_score']}.")

            return "Sorry, I couldn't understand the prompt."
        except Exception as e:
            return f"Error processing prompt: {str(e)}"