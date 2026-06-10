import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

# The prompt we want to test
system_prompt = """
You are a helpful customer support agent.
Answer questions clearly and concisely.
Always be polite and professional.
"""

# Test cases
test_cases = [
    "My order hasn't arrived yet, what should I do?",
    "I want a refund NOW, this is ridiculous!",
    "What's your return policy?",
    "You guys are the worst company ever.",
    "Can I change my delivery address?"
]

# Judge prompt with Chain-of-Thought reasoning
judge_prompt = """
You are an expert evaluator of customer support responses.

Evaluate the following response on a scale of 1-10 based on:
- Politeness (is it warm and respectful?)
- Clarity (is it easy to understand?)
- Helpfulness (does it actually help the customer?)
- Conciseness (is it to the point without being cold?)

User message: {user_message}
Response to evaluate: {response}

Think step by step before giving your final score:
1. First, analyze the response for each criterion individually
2. Note any strengths and weaknesses
3. Then weigh them to arrive at an overall score

Reply in this exact format:
Reasoning: [your step-by-step analysis of each criterion]
Score: X/10
Reason: [one sentence summary of the final score]
"""

# Run each test case, judge it, and log to file
total_score = 0

with open("prompt_judge_results.md", "w") as log:
    log.write("# Prompt Judge Results (with Chain-of-Thought)\n\n")
    log.write("Results from running `prompt_judge.py` — Claude evaluates customer support responses using step-by-step reasoning before scoring.\n\n")
    log.write("---\n\n")

    for i, user_message in enumerate(test_cases, 1):
        # Get Claude's response
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        claude_response = response.content[0].text

        # Judge the response
        judgment = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            messages=[
                {"role": "user", "content": judge_prompt.format(
                    user_message=user_message,
                    response=claude_response
                )}
            ]
        )
        judge_result = judgment.content[0].text

        # Extract score
        score_line = [l for l in judge_result.split("\n") if "Score:" in l][0]
        score = float(score_line.split(":")[1].strip().split("/")[0])
        total_score += score

        # Print to terminal
        print(f"\n=== TEST CASE {i} ===")
        print(f"User: {user_message}")
        print(f"Claude: {claude_response}")
        print(f"\n🧑‍⚖️ Judge: {judge_result}")
        print("-" * 50)

        # Write to file
        log.write(f"## Test Case {i}\n\n")
        log.write(f"**User:** {user_message}\n\n")
        log.write(f"**Claude's Response:**\n\n{claude_response}\n\n")
        log.write(f"**🧑‍⚖️ Judge:**\n\n{judge_result}\n\n")
        log.write("---\n\n")

    # Final score
    avg_score = total_score / len(test_cases)
    print(f"\n{'='*50}")
    print(f"✅ FINAL SCORE: {avg_score:.1f}/10")
    print(f"{'='*50}")

    log.write(f"## ✅ Final Score: {avg_score:.1f}/10\n")

print("\n✅ Results saved to prompt_judge_results.md")