import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


# Multi-turn conversations with tricky edge cases
conversations = [
    [
        {"role": "user", "content": "I just got a new pomeranian!"},
        {
            "role": "assistant",
            "content": "Congratulations on your new furry friend! Is this your first dog?",
        },
        {"role": "user", "content": "Yes, it is. I named her Luna."},
        {
            "role": "assistant",
            "content": "Luna is a lovely name! As a first-time dog owner, you might have some questions. What would you like to know about caring for Luna?",
        },
        {
            "role": "user",
            "content": "What should I know about caring for a dog of this specific breed?",
        },  # Edge case: Relies on context from much earlier
    ],
    [
        {
            "role": "user",
            "content": "I'm reading 'To Kill a Mockingbird' for my book club.",
        },
        {
            "role": "assistant",
            "content": "Great choice! 'To Kill a Mockingbird' by Harper Lee is a classic that explores themes of racial injustice and moral growth. How are you finding it so far?",
        },
        {
            "role": "user",
            "content": "It's powerful. Hey, when was Scout's birthday again?",
        },  # Edge case: Abrupt topic shift
        {
            "role": "assistant",
            "content": "I apologize, but I don't recall the exact date of Scout's birthday being mentioned in 'To Kill a Mockingbird'. The novel doesn't focus on such specific details. Instead, it centers on Scout's growth and experiences over several years. Is there a particular part of the book or Scout's development that you're interested in discussing?",
        },
        {
            "role": "user",
            "content": "Oh, right. Well, can you suggest a recipe for a classic Southern cake?",
        },  # Edge case: Another topic shift
    ],
]


# Get Claude's response to a multi-turn conversation
def get_completion(conversation: list):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=conversation,
    )
    return message.content[0].text


# Evaluate response on a 1-5 ordinal scale for context utilization
def evaluate_ordinal(model_output, conversation):
    conversation_text = "".join(
        f"{turn['role']}: {turn['content']}\n" for turn in conversation
    )

    ordinal_prompt = f"""Rate how well this response utilizes the conversation context on a scale of 1-5:

<conversation>
{conversation_text}
</conversation>

<response>{model_output}</response>

1: Completely ignores context
2: Poor context use
3: Some context use
4: Good context use
5: Perfectly utilizes context

Think through your reasoning in <thinking> tags, then output only the number in <score> tags."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": ordinal_prompt}],
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
with open("ordinal_eval_results.md", "w") as log:
    log.write("# Ordinal Eval Results — Context Utilization\n\n")
    log.write("Results from running `ordinal_eval.py` — Claude evaluates how well its own responses use prior conversation context, on a 1-5 ordinal scale.\n\n")
    log.write("---\n\n")

    scores = []

    for i, conversation in enumerate(conversations, 1):
        # Get Claude's response to the conversation
        output = get_completion(conversation)

        # Grade it
        score, reasoning = evaluate_ordinal(output, conversation)
        scores.append(score)

        # Print to terminal
        print(f"\n=== CONVERSATION {i} ===")
        print(f"Last user message: {conversation[-1]['content']}")
        print(f"Claude's Response: {output}")
        print(f"Score: {score}/5")
        print("-" * 60)

        # Write to file
        log.write(f"## Conversation {i}\n\n")
        log.write("**Conversation history:**\n\n")
        for turn in conversation:
            log.write(f"- **{turn['role']}:** {turn['content']}\n")
        log.write(f"\n**Claude's Response:**\n\n{output}\n\n")
        log.write(f"**Judge's Reasoning:**\n\n{reasoning}\n\n")
        log.write(f"**Score:** {score}/5\n\n")
        log.write("---\n\n")

    # Final average
    average_score = sum(scores) / len(scores)
    print(f"\n{'='*60}")
    print(f"✅ AVERAGE CONTEXT UTILIZATION SCORE: {average_score:.1f}/5")
    print(f"{'='*60}")

    log.write(f"## ✅ Average Context Utilization Score: {average_score:.1f}/5\n\n")
    log.write("## Key Takeaway\n\n")
    log.write("Ordinal grading (1-5) sits between binary (correct/incorrect) and full numeric scoring (1-10). It captures nuance — better than yes/no — without the inconsistency of fine-grained scoring. It's well-suited for **subjective quality dimensions** like context utilization, tone, or coherence, where degrees of quality matter but exact decimals don't.\n")

print("\n✅ Results saved to ordinal_eval_results.md")