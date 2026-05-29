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

# Multiple test cases to stress test the prompt
test_cases = [
    "My order hasn't arrived yet, what should I do?",
    "I want a refund NOW, this is ridiculous!",
    "What's your return policy?",
    "You guys are the worst company ever.",
    "Can I change my delivery address?"
]

# Run each test case
for i, user_message in enumerate(test_cases, 1):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    print(f"\n=== TEST CASE {i} ===")
    print(f"User: {user_message}")
    print(f"Claude: {response.content[0].text}")
    print("-" * 50)

# Send it to Claude
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_message}
    ]
)

print("=== PROMPT BEING TESTED ===")
print(system_prompt)
print("=== USER MESSAGE ===")
print(user_message)
print("=== CLAUDE'S RESPONSE ===")
print(response.content[0].text)