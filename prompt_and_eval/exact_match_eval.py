import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


# Tweets with their correct sentiment classification
tweets = [
    {
        "text": "This movie was a total waste of time. 👎",
        "sentiment": "negative",
    },
    {
        "text": "The new album is 🔥! Been on repeat all day.",
        "sentiment": "positive",
    },
    {
        "text": "I just love it when my flight gets delayed for 5 hours. #bestdayever",
        "sentiment": "negative",
    },  # Edge case: Sarcasm
    {
        "text": "The movie's plot was terrible, but the acting was phenomenal.",
        "sentiment": "mixed",
    },  # Edge case: Mixed sentiment
    {
        "text": "The meeting is scheduled for 3 PM tomorrow.",
        "sentiment": "neutral",
    },  # Edge case: Pure neutral statement
]


# Get Claude's classification — we constrain output to a fixed set of labels
def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=50,  # Short response — we only need one word
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# Exact match — the strictest, fastest eval
def evaluate_exact_match(model_output, correct_answer):
    return model_output.strip().lower() == correct_answer.lower()


# Run all evals and log to file
with open("exact_match_eval_results.md", "w") as log:
    log.write("# Exact Match Eval Results — Sentiment Classification\n\n")
    log.write("Results from running `exact_match_eval.py` — the strictest and cheapest eval pattern. Claude classifies tweets into one of `positive`, `negative`, `neutral`, or `mixed`, and the eval checks if the output exactly matches the expected label.\n\n")
    log.write("---\n\n")

    correct_count = 0
    total = len(tweets)

    for i, tweet in enumerate(tweets, 1):
        text = tweet["text"]
        expected = tweet["sentiment"]

        # Get Claude's classification
        prompt = f"Classify this as 'positive', 'negative', 'neutral', or 'mixed'. Reply with only one word: {text}"
        output = get_completion(prompt)

        # Check exact match
        is_correct = evaluate_exact_match(output, expected)
        if is_correct:
            correct_count += 1

        verdict = "✅ CORRECT" if is_correct else "❌ INCORRECT"

        # Print to terminal
        print(f"\n=== TWEET {i} ===")
        print(f"Text: {text}")
        print(f"Expected: {expected}")
        print(f"Claude said: {output.strip()}")
        print(f"Verdict: {verdict}")
        print("-" * 60)

        # Write to file
        log.write(f"## Tweet {i}\n\n")
        log.write(f"**Text:** {text}\n\n")
        log.write(f"**Expected Sentiment:** {expected}\n\n")
        log.write(f"**Claude's Classification:** {output.strip()}\n\n")
        log.write(f"**Verdict:** {verdict}\n\n")
        log.write("---\n\n")

    # Final score
    accuracy = (correct_count / total) * 100
    print(f"\n{'='*60}")
    print(f"✅ SENTIMENT ANALYSIS ACCURACY: {correct_count}/{total} correct ({accuracy:.1f}%)")
    print(f"{'='*60}")

    log.write(f"## ✅ Sentiment Analysis Accuracy: {correct_count}/{total} correct ({accuracy:.1f}%)\n\n")
    log.write("## When Exact Match Works\n\n")
    log.write("Exact match is the right tool when the output is one of a **fixed set of categories**:\n\n")
    log.write("- Sentiment classification (`positive`, `negative`, `neutral`, `mixed`)\n")
    log.write("- Intent classification (`refund`, `complaint`, `question`, etc.)\n")
    log.write("- Spam detection (`spam`, `not spam`)\n")
    log.write("- Multiple choice answers (`A`, `B`, `C`, `D`)\n\n")
    log.write("## When Exact Match Fails\n\n")
    log.write("It's a poor choice for open-ended tasks:\n\n")
    log.write("- Long answers — `\"Paris\"` won't match `\"The capital of France is Paris\"`\n")
    log.write("- Free-form text — too many ways to say the same thing\n")
    log.write("- Subjective tasks — there's no single right answer\n\n")
    log.write("For those, use an LLM-as-judge (`binary_eval.py`), ROUGE, or cosine similarity.\n\n")
    log.write("## Key Takeaway\n\n")
    log.write("**Use the strictest eval that fits the task.** Exact match is the fastest and cheapest pattern — no LLM call, no math, just a string comparison. When your task is constrained to a fixed set of labels, exact match is hard to beat.\n")

print("\n✅ Results saved to exact_match_eval_results.md")