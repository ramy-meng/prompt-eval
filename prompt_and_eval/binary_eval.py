import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


# Build the grader prompt — Claude grades the answer against the golden answer
def build_grader_prompt(answer, rubric):
    return f"""Grade this answer based on the rubric:

<rubric>{rubric}</rubric>

<answer>{answer}</answer>

Think through your reasoning in <thinking> tags, then output 'correct' or 'incorrect' in <result> tags."""


# Grade a single completion — returns "correct" or "incorrect"
def grade_completion(output, golden_answer):
    grader_response = (
        client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": build_grader_prompt(output, golden_answer)}
            ],
        )
        .content[0]
        .text
    )
    return (
        "correct"
        if "<result>correct</result>" in grader_response.lower()
        else "incorrect"
    ), grader_response


# Get Claude's answer to a question
def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# Evaluation data — each test case has a question and a golden answer
eval_data = [
    {
        "question": "Is 42 the answer to life, the universe, and everything?",
        "golden_answer": "Yes, according to 'The Hitchhiker's Guide to the Galaxy'.",
    },
    {
        "question": "What is the capital of France?",
        "golden_answer": "The capital of France is Paris.",
    },
    {
        "question": "What is 2 + 2?",
        "golden_answer": "4",
    },
    {
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "golden_answer": "William Shakespeare",
    },
]


# Run all evals and log results
with open("binary_eval_results.md", "w") as log:
    log.write("# Binary Eval Results\n\n")
    log.write("Results from running `binary_eval.py` — Claude evaluates its own answers against golden answers using a binary correct/incorrect grading system.\n\n")
    log.write("---\n\n")

    correct_count = 0
    total = len(eval_data)

    for i, item in enumerate(eval_data, 1):
        question = item["question"]
        golden_answer = item["golden_answer"]

        # Get Claude's answer
        output = get_completion(question)

        # Grade it
        verdict, reasoning = grade_completion(output, golden_answer)

        if verdict == "correct":
            correct_count += 1

        # Print to terminal
        print(f"\n=== TEST CASE {i} ===")
        print(f"Question: {question}")
        print(f"Golden Answer: {golden_answer}")
        print(f"Claude's Answer: {output}")
        print(f"Verdict: {verdict.upper()}")
        print("-" * 60)

        # Write to file
        log.write(f"## Test Case {i}\n\n")
        log.write(f"**Question:** {question}\n\n")
        log.write(f"**Golden Answer:** {golden_answer}\n\n")
        log.write(f"**Claude's Answer:**\n\n{output}\n\n")
        log.write(f"**Judge's Reasoning:**\n\n{reasoning}\n\n")
        log.write(f"**Verdict:** {verdict.upper()}\n\n")
        log.write("---\n\n")

    # Final score
    score_percent = (correct_count / total) * 100
    print(f"\n{'='*60}")
    print(f"✅ FINAL SCORE: {correct_count}/{total} correct ({score_percent:.1f}%)")
    print(f"{'='*60}")

    log.write(f"## ✅ Final Score: {correct_count}/{total} correct ({score_percent:.1f}%)\n\n")
    log.write("## Key Takeaway\n\n")
    log.write("Binary eval is ideal when there's a known correct answer. Unlike subjective scoring (1-10), it gives a fast, consistent yes/no verdict — perfect for measuring **factual accuracy**. For quality dimensions like tone, clarity, or helpfulness, scale-based evals (like `prompt_judge.py`) are a better fit.\n")

print("\n✅ Results saved to binary_eval_results.md")