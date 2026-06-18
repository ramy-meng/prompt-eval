import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


# Customer inquiries, each with a target tone the response should match
inquiries = [
    {
        "text": "This is the third time you've messed up my order. I want a refund NOW!",
        "tone": "empathetic",
    },  # Edge case: Angry customer
    {
        "text": "I tried resetting my password but then my account got locked, and now I can't access any of my settings.",
        "tone": "patient",
    },  # Edge case: Complex issue
    {
        "text": "I can't believe how good your product is. It's ruined all others for me!",
        "tone": "professional",
    },  # Edge case: Compliment as complaint
]


# Get Claude's response to a customer inquiry
def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# Evaluate response on a 1-5 Likert scale against a target tone
def evaluate_likert(model_output, target_tone):
    tone_prompt = f"""Rate this customer service response on a scale of 1-5 for being {target_tone}:

<response>{model_output}</response>

1: Not at all {target_tone}
2: Slightly {target_tone}
3: Somewhat {target_tone}
4: Mostly {target_tone}
5: Perfectly {target_tone}

Think through your reasoning in <thinking> tags, then output only the number in <score> tags."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": tone_prompt}],
    )
    text = response.content[0].text

    # Extract score from <score> tags
    try:
        score_start = text.index("<score>") + len("<score>")
        score_end = text.index("</score>")
        score = int(text[score_start:score_end].strip())
    except (ValueError, IndexError):
        score = 0  # Fallback if parsing fails

    return score, text


# Run all evals and log to file
with open("likert_eval_results.md", "w") as log:
    log.write("# Likert Eval Results — Tone Matching\n\n")
    log.write("Results from running `likert_eval.py` — Claude evaluates how well its own responses match a **target tone** on a 1-5 Likert scale. This pattern is useful when the right response depends on context (an angry customer needs empathy, a complex issue needs patience, etc).\n\n")
    log.write("---\n\n")

    scores = []

    for i, inquiry in enumerate(inquiries, 1):
        text = inquiry["text"]
        target_tone = inquiry["tone"]

        # Get Claude's response
        output = get_completion(f"Respond to this customer inquiry: {text}")

        # Grade it on tone match
        score, reasoning = evaluate_likert(output, target_tone)
        scores.append(score)

        # Print to terminal
        print(f"\n=== INQUIRY {i} ===")
        print(f"Customer: {text}")
        print(f"Target Tone: {target_tone}")
        print(f"Claude's Response: {output}")
        print(f"Tone Match Score: {score}/5")
        print("-" * 60)

        # Write to file
        log.write(f"## Inquiry {i}\n\n")
        log.write(f"**Customer:** {text}\n\n")
        log.write(f"**Target Tone:** {target_tone}\n\n")
        log.write(f"**Claude's Response:**\n\n{output}\n\n")
        log.write(f"**Judge's Reasoning:**\n\n{reasoning}\n\n")
        log.write(f"**Tone Match Score:** {score}/5\n\n")
        log.write("---\n\n")

    # Final average
    average_score = sum(scores) / len(scores)
    print(f"\n{'='*60}")
    print(f"✅ AVERAGE TONE MATCH SCORE: {average_score:.1f}/5")
    print(f"{'='*60}")

    log.write(f"## ✅ Average Tone Match Score: {average_score:.1f}/5\n\n")
    log.write("## Key Takeaway\n\n")
    log.write("Likert scales are borrowed from survey methodology and measure **how strongly something matches a target quality**. They're especially useful when:\n\n")
    log.write("- The 'right' response depends on context (different tone for different customers)\n")
    log.write("- You're measuring a **specific trait** rather than overall quality\n")
    log.write("- You need finer granularity than binary, but less variance than 1-10\n\n")
    log.write("In production, this pattern can power dynamic prompt selection — Claude analyzes the customer's message, picks the right tone, and the eval verifies that tone was actually delivered.\n")

print("\n✅ Results saved to likert_eval_results.md")