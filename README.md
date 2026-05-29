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

## Project Structure

```
prompt-eval/
├── eval.py                    # Main eval system — compares prompts head-to-head
├── simple_eval.py             # Single prompt eval against multiple test cases
├── diff_prompt_same_test.py   # A/B prompt comparison experiments
├── test.py                    # First API call test
├── .env.example               # Environment variable template
└── .gitignore                 # Keeps API key out of version control
```

## Setup

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

**4. Run the eval**
```bash
python3 eval.py
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
| Prompt A | Original — polite and professional | 8.0/10 |
| Prompt B | Empathetic — acknowledge feelings first | 8.4/10 |
| Prompt C | Conversational — no markdown, no emojis when angry | 9.0/10 |

**Winner: Prompt C** — The judge consistently flagged over-formatting and misplaced emojis as weaknesses. Prompt C addressed both and scored a full point higher.

## Key Insight

The judge has no memory of writing the response it evaluates. By giving Claude a different persona (evaluator vs. agent), it assesses the output neutrally — the same principle behind Constitutional AI and RLHF.

## Built With

- [Anthropic API](https://docs.anthropic.com)
- Python 3
- python-dotenv