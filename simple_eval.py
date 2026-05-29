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

# Judge prompt
judge_prompt = """
You are an expert evaluator of customer support responses.

Score the following response on a scale of 1-10 based on:
- Politeness (is it warm and respectful?)
- Clarity (is it easy to understand?)
- Helpfulness (does it actually help the customer?)
- Conciseness (is it to the point without being cold?)

User message: {user_message}
Response to evaluate: {response}

Reply in this exact format:
Score: X/10
Reason: [one sentence explanation]
"""

# Run each test case and judge it
total_score = 0

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
        max_tokens=256,
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

    print(f"\n=== TEST CASE {i} ===")
    print(f"User: {user_message}")
    print(f"Claude: {claude_response}")
    print(f"\n🧑‍⚖️ Judge: {judge_result}")
    print("-" * 50)

# Final score
avg_score = total_score / len(test_cases)
print(f"\n{'='*50}")
print(f"✅ FINAL SCORE: {avg_score:.1f}/10")
print(f"{'='*50}")