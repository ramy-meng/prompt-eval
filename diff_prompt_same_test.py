import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

# PROMPT A - original
prompt_a = """
You are a helpful customer support agent.
Answer questions clearly and concisely.
Always be polite and professional.
"""

# PROMPT B - more empathetic version
prompt_b = """
You are a warm and empathetic customer support agent.
Always acknowledge the customer's feelings first before solving their problem.
Use simple language, avoid jargon, and keep responses brief.
If you don't know something, be honest and direct them to the right place.
"""

# PROMPT C - addresses judge feedback
prompt_c = """
You are a friendly customer support agent.
Keep responses short and conversational — no bullet points or headers unless absolutely necessary.
Acknowledge the customer's feelings first, then solve the problem in plain language.
If a customer is angry or frustrated, skip emojis and be calm and direct.
If you don't know something, be honest and point them in the right direction.
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

def run_eval(prompt, prompt_name):
    print(f"\n{'='*50}")
    print(f"TESTING: {prompt_name}")
    print(f"{'='*50}")
    
    total_score = 0
    
    for i, user_message in enumerate(test_cases, 1):
        # Get Claude's response
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=prompt,
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

        print(f"\n--- Test Case {i} ---")
        print(f"User: {user_message}")
        print(f"Claude: {claude_response}")
        print(f"🧑‍⚖️ {judge_result}")

    avg_score = total_score / len(test_cases)
    print(f"\n✅ {prompt_name} FINAL SCORE: {avg_score:.1f}/10")
    return avg_score

# Run all three prompts
score_a = run_eval(prompt_a, "PROMPT A (Original)")
score_b = run_eval(prompt_b, "PROMPT B (Empathetic)")
score_c = run_eval(prompt_c, "PROMPT C (Conversational)")

# Winner
scores = {"PROMPT A": score_a, "PROMPT B": score_b, "PROMPT C": score_c}
winner = max(scores, key=scores.get)

print(f"\n{'='*50}")
print(f"🏆 WINNER: {winner}")
print(f"Prompt A: {score_a:.1f}/10")
print(f"Prompt B: {score_b:.1f}/10")
print(f"Prompt C: {score_c:.1f}/10")
print(f"{'='*50}")