# Prompt Eval System

A prompt evaluation system built with the Anthropic API that uses Claude as an automated judge (LLM-as-judge pattern) to score and compare prompt performance across multiple test cases. Also includes a minimal RAG (Retrieval-Augmented Generation) demo showing how to give Claude context to answer domain-specific questions, and a Chain-of-Thought (CoT) version of the judge that shows step-by-step reasoning before scoring.

## What It Does

- Runs a system prompt against multiple test cases
- Uses a second Claude instance as an impartial judge to score each response
- Compares multiple prompts head-to-head and declares a winner
- Produces a final aggregate score to measure prompt quality objectively
- Demonstrates RAG by augmenting Claude with a company FAQ as context
- Demonstrates Chain-of-Thought (CoT) prompting to make the judge more transparent and accurate

## What I Learned

- How to use the Anthropic API end-to-end
- The LLM-as-judge pattern used in real AI evaluation pipelines
- How to iterate on prompts using data instead of guesswork
- Why prompt scoring has variance and how to account for it
- How Retrieval-Augmented Generation (RAG) gives Claude context for domain-specific questions
- How Chain-of-Thought reasoning improves transparency and surfaces hidden weaknesses
- How Constitutional AI uses similar principles at training scale

## Want to See the Results Without Running the Code?

Check out the results files for the full breakdown — all test cases, judge scores, and key takeaways. No API key or setup needed.

- [`prompt_and_eval/prompt_comparison_results.md`](./prompt_and_eval/prompt_comparison_results.md) — prompt eval results
- [`prompt_and_eval/prompt_judge_results.md`](./prompt_and_eval/prompt_judge_results.md) — Chain-of-Thought judge results
- [`rag/rag_results.md`](./rag/rag_results.md) — RAG demo results

## Project Structure

```
prompt-eval/
├── prompt_and_eval/
│   ├── prompt_comparison.py            # Compares Prompt A vs B vs C head-to-head with scores
│   ├── prompt_judge.py                 # Single-prompt eval with baseline judge
│   ├── prompt_judge_cot.py             # Same eval but with Chain-of-Thought reasoning
│   ├── prompt_runner.py                # Runs a prompt against test cases, no judge
│   ├── test.py                         # First API call — verifies setup works
│   ├── prompt_comparison_results.md    # Full prompt comparison results
│   └── prompt_judge_results.md         # Chain-of-Thought judge results
├── rag/
│   ├── rag_demo.py                     # Minimal RAG system using a company FAQ as context
│   ├── company_faq.txt                 # Sample knowledge base for the RAG demo
│   └── rag_results.md                  # RAG demo results
├── .env.example                        # Environment variable template
└── .gitignore                          # Keeps API key out of version control
```

## Setup

> **Note:** Running the code requires an Anthropic API key. You can get one at [console.anthropic.com](https://console.anthropic.com) — $5 in credits is more than enough to run all the scripts. If you just want to read the results, see the result markdown files above instead.

**1. Clone the repo**
```bash
git clone https://github.com/ramy-meng/prompt-eval.git
cd prompt-eval
```

**2. Install dependencies**
```bash
pip install anthropic python-dotenv
```

**3. Add your API key**
```bash
cp .env.example .env
```
Open `.env` and replace `your-api-key-here` with your actual Anthropic API key from [console.anthropic.com](https://console.anthropic.com).

**4. Run the files**
```bash
# Verify your setup works
python3 prompt_and_eval/test.py

# Run a prompt against test cases (no scoring)
python3 prompt_and_eval/prompt_runner.py

# Run a prompt and get an automated score (baseline judge)
python3 prompt_and_eval/prompt_judge.py

# Run the same eval with a Chain-of-Thought judge
python3 prompt_and_eval/prompt_judge_cot.py

# Compare Prompt A vs B vs C and see the winner
python3 prompt_and_eval/prompt_comparison.py

# Run the RAG demo using the company FAQ as context
python3 rag/rag_demo.py
```

## How It Works

### Prompt Eval (LLM-as-Judge)

**Step 1 — The Agent**
Claude is given a system prompt and responds to customer support messages.

**Step 2 — The Judge**
A second Claude call evaluates the response on four criteria:
- **Politeness** — is it warm and respectful?
- **Clarity** — is it easy to understand?
- **Helpfulness** — does it actually solve the problem?
- **Conciseness** — is it to the point without being cold?

**Step 3 — Compare & Iterate**
Prompts are scored and ranked. The winning prompt is the one that consistently scores highest across all test cases.

### Chain-of-Thought (CoT) Judge

The CoT version asks the judge to **reason through each criterion individually before scoring**. This produces more transparent, more accurate, and more honest evaluations — though it is slower and uses more tokens.

**Trade-offs:**
- ✅ More accurate and consistent scoring
- ✅ Transparent reasoning you can debug
- ❌ Slower response time
- ❌ Higher token cost

### RAG Demo

**Step 1 — Retrieval**
Load relevant content from `company_faq.txt`.

**Step 2 — Augmented**
Stuff the relevant content into the prompt as context.

**Step 3 — Generation**
Claude answers the user's question based on the provided context — and honestly says "I don't know" when the answer isn't in the FAQ.

## Results

### Prompt Comparison

After iterating through three prompts:

| Prompt | Description | Score |
|--------|-------------|-------|
| Prompt A | Original — polite and professional | 8.2/10 |
| Prompt B | Empathetic — acknowledge feelings first | 8.4/10 |
| Prompt C | Conversational — no markdown, no emojis when angry | 9.0/10 |

**Winner: Prompt C** — The judge consistently flagged over-formatting and misplaced emojis as weaknesses. Prompt C addressed both and scored a full point higher.

See the full breakdown in [`prompt_and_eval/prompt_comparison_results.md`](./prompt_and_eval/prompt_comparison_results.md).

### Chain-of-Thought Judge

Adding CoT to the judge made the evaluations more rigorous. One test case dropped from 8/10 (baseline) to 6/10 (CoT) — not because the response got worse, but because the CoT judge couldn't hand-wave weaknesses anymore. It had to defend each criterion individually, surfacing problems (like over-formatting) that the baseline judge glossed over.

This mirrors a key insight from the Constitutional AI paper:

> *"Both the SL and RL methods can leverage chain-of-thought style reasoning to improve the human-judged performance and transparency of AI decision making."*

See the full breakdown in [`prompt_and_eval/prompt_judge_results.md`](./prompt_and_eval/prompt_judge_results.md).

### RAG Demo

Claude correctly answered 3 questions using the FAQ as context and honestly admitted it didn't know the dress code (not in the FAQ) instead of making something up — exactly the "harmless but non-evasive" behavior the Anthropic Model Spec describes.

See the full breakdown in [`rag/rag_results.md`](./rag/rag_results.md).

## Key Insight

The judge has no memory of writing the response it evaluates. By giving Claude a different persona (evaluator vs. agent), it assesses the output neutrally — the same principle behind Constitutional AI and RLHF. Adding Chain-of-Thought reasoning to that judge makes the evaluation even more transparent and accurate, at the cost of speed and tokens.

## Built With

- [Anthropic API](https://docs.anthropic.com)
- Python 3
- python-dotenv