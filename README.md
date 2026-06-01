# Prompt Eval System

A prompt evaluation system built with the Anthropic API that uses Claude as an automated judge (LLM-as-judge pattern) to score and compare prompt performance across multiple test cases.

## What It Does

- Runs a system prompt against multiple test cases
- Uses a second Claude instance as an impartial judge to score each response
- Compares multiple prompts head-to-head and declares a winner
- Produces a final aggregate score to measure prompt quality objectively

## What I Learned

- How to use the Anthropic API end-to-end
- The LLM-as-judge pattern used in real AI evaluation pipelines
- How to iterate on prompts using data instead of guesswork
- Why prompt scoring has variance and how to account for it

## Want to See the Results Without Running the Code?

Check out [`prompt_comparison_results.md`](./prompt_comparison_results.md) for the full breakdown — all test cases, judge scores, and key takeaways. No API key or setup needed.

## Project Structure

```
prompt-eval/
├── prompt_comparison.py            # Compares Prompt A vs B vs C head-to-head with scores
├── prompt_judge.py                 # Runs a single prompt through the LLM-as-judge eval
├── prompt_runner.py                # Runs a prompt against test cases, no judge
├── test.py                         # First API call — verifies setup works
├── prompt_comparison_results.md    # Full eval results — readable without running the code
├── .env.example                    # Environment variable template
└── .gitignore                      # Keeps API key out of version control
```

## Setup

> **Note:** Running the code requires an Anthropic API key. You can get one at [console.anthropic.com](https://console.anthropic.com) — $5 in credits is more than enough to run all the scripts. If you just want to read the results, see [`prompt_comparison_results.md`](./prompt_comparison_results.md) instead.

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
python3 test.py

# Run a prompt against test cases (no scoring)
python3 prompt_runner.py

# Run a prompt and get an automated score
python3 prompt_judge.py

# Compare Prompt A vs B vs C and see the winner
python3 prompt_comparison.py
```

## How It Works

### Step 1 — The Agent
Claude is given a system prompt and responds to customer support messages.

### Step 2 — The Judge
A second Claude call evaluates the response on four criteria:
- **Politeness** — is it warm and respectful?
- **Clarity** — is it easy to understand?
- **Helpfulness** — does it actually solve the problem?
- **Conciseness** — is it to the point without being cold?

### Step 3 — Compare & Iterate
Prompts are scored and ranked. The winning prompt is the one that consistently scores highest across all test cases.

## Results

After iterating through three prompts:

| Prompt | Description | Score |
|--------|-------------|-------|
| Prompt A | Original — polite and professional | 8.2/10 |
| Prompt B | Empathetic — acknowledge feelings first | 8.4/10 |
| Prompt C | Conversational — no markdown, no emojis when angry | 9.0/10 |

**Winner: Prompt C** — The judge consistently flagged over-formatting and misplaced emojis as weaknesses. Prompt C addressed both and scored a full point higher.

See the full breakdown in [`prompt_comparison_results.md`](./prompt_comparison_results.md).

## Key Insight

The judge has no memory of writing the response it evaluates. By giving Claude a different persona (evaluator vs. agent), it assesses the output neutrally — the same principle behind Constitutional AI and RLHF.

## Built With

- [Anthropic API](https://docs.anthropic.com)
- Python 3
- python-dotenv