# Prompt Eval System

A comprehensive prompt evaluation and prompt engineering project built with the Anthropic API. It demonstrates eight major eval patterns used by real AI teams — LLM-as-judge, Chain-of-Thought, binary, ordinal, classification, Likert, ROUGE-L, cosine similarity, and exact match — alongside a Retrieval-Augmented Generation (RAG) demo and a semantic search system using embeddings.

## What It Does

- Runs system prompts against multiple test cases
- Uses Claude as an automated judge (LLM-as-judge pattern) to score responses
- Compares multiple prompts head-to-head and declares a winner
- Demonstrates **eight different eval patterns** — from strict exact match to nuanced scale-based grading
- Demonstrates RAG by augmenting Claude with a company FAQ as context
- Demonstrates Chain-of-Thought (CoT) prompting to make the judge more transparent
- Demonstrates semantic search using Voyage AI embeddings + cosine similarity

## What I Learned

- How to use the Anthropic API end-to-end
- The LLM-as-judge pattern used in real AI evaluation pipelines
- When to use **strict** vs **loose** evals — exact match vs scale-based grading
- The difference between LLM-judged and metric-based evals (ROUGE, cosine similarity)
- How to iterate on prompts using data instead of guesswork
- How Retrieval-Augmented Generation (RAG) gives Claude context for domain-specific questions
- How Chain-of-Thought reasoning improves transparency and surfaces hidden weaknesses
- How embeddings turn text into vectors so meaning can be compared mathematically — for both retrieval (semantic search) and measurement (consistency checks)
- How Constitutional AI uses similar principles at training scale

## The Eight Eval Patterns

This project implements every major eval pattern a prompt engineer uses in production:

| File | Pattern | Evaluator | Best For |
|------|---------|-----------|----------|
| `prompt_judge.py` | Scale (1-10) | LLM judge | Overall response quality |
| `prompt_judge_cot.py` | Scale + Chain-of-Thought | LLM judge | Transparent quality grading |
| `binary_eval.py` | Binary (correct / incorrect) | LLM judge | Factual accuracy with golden answers |
| `ordinal_eval.py` | Ordinal (1-5) | LLM judge | Degree of quality (e.g. context utilization) |
| `classification_eval.py` | Classification (compliant / not) | LLM judge | Safety & compliance (e.g. PHI leakage) |
| `likert_eval.py` | Likert (1-5 trait) | LLM judge | Matching a target trait (e.g. tone) |
| `rouge_eval.py` | ROUGE-L F1 | Pure math | Summarization vs reference |
| `cosine_similarity_eval.py` | Cosine similarity | Embeddings | Response consistency across phrasings |
| `exact_match_eval.py` | Exact match | String compare | Classification tasks (sentiment, intent) |

**The principle:** use the strictest eval that fits your task. Exact match is fastest and cheapest when it applies. LLM judges are more flexible but cost more.

## Want to See the Results Without Running the Code?

Each eval generates a markdown results file with full details — test cases, responses, judge reasoning, and final scores. No API key or setup needed.

- [`prompt_and_eval/prompt_comparison_results.md`](./prompt_and_eval/prompt_comparison_results.md)
- [`prompt_and_eval/prompt_judge_results.md`](./prompt_and_eval/prompt_judge_results.md)
- [`prompt_and_eval/binary_eval_results.md`](./prompt_and_eval/binary_eval_results.md)
- [`prompt_and_eval/ordinal_eval_results.md`](./prompt_and_eval/ordinal_eval_results.md)
- [`prompt_and_eval/classification_eval_results.md`](./prompt_and_eval/classification_eval_results.md)
- [`prompt_and_eval/likert_eval_results.md`](./prompt_and_eval/likert_eval_results.md)
- [`prompt_and_eval/rouge_eval_results.md`](./prompt_and_eval/rouge_eval_results.md)
- [`prompt_and_eval/cosine_similarity_eval_results.md`](./prompt_and_eval/cosine_similarity_eval_results.md)
- [`prompt_and_eval/exact_match_eval_results.md`](./prompt_and_eval/exact_match_eval_results.md)
- [`rag/rag_results.md`](./rag/rag_results.md)
- [`rag/semantic_search_results.md`](./rag/semantic_search_results.md)

## Project Structure

```
prompt-eval/
├── prompt_and_eval/
│   ├── prompt_comparison.py            # Compares Prompt A vs B vs C head-to-head
│   ├── prompt_judge.py                 # Scale-based eval with baseline judge
│   ├── prompt_judge_cot.py             # Same eval with Chain-of-Thought reasoning
│   ├── prompt_runner.py                # Runs a prompt against test cases, no judge
│   ├── binary_eval.py                  # Binary correct/incorrect with golden answers
│   ├── ordinal_eval.py                 # 1-5 ordinal scale for context utilization
│   ├── classification_eval.py          # Compliance / safety eval (PHI leakage)
│   ├── likert_eval.py                  # 1-5 Likert trait eval (target tone matching)
│   ├── rouge_eval.py                   # ROUGE-L F1 for summarization
│   ├── cosine_similarity_eval.py       # Consistency check using embeddings
│   ├── exact_match_eval.py             # Strict string match for classification
│   ├── test.py                         # First API call — verifies setup works
│   └── *_results.md                    # Generated result files per eval
├── rag/
│   ├── rag_demo.py                     # Minimal RAG system using a company FAQ as context
│   ├── semantic_search.py              # Embeddings + cosine similarity for chunk retrieval
│   ├── company_faq.txt                 # Sample knowledge base for the RAG demo
│   ├── rag_results.md                  # RAG demo results
│   └── semantic_search_results.md      # Semantic search results
├── .env.example                        # Environment variable template
└── .gitignore                          # Keeps API key out of version control
```

## Setup

> **Note:** Running the code requires an Anthropic API key. You can get one at [console.anthropic.com](https://console.anthropic.com) — $5 in credits is more than enough to run all the scripts. The semantic search demo also requires a free Voyage AI API key from [voyageai.com](https://www.voyageai.com/). If you just want to read the results, see the result markdown files above instead.

**1. Clone the repo**
```bash
git clone https://github.com/ramy-meng/prompt-eval.git
cd prompt-eval
```

**2. Install dependencies**
```bash
pip install anthropic python-dotenv voyageai rouge sentence-transformers
```

**3. Add your API keys**
```bash
cp .env.example .env
```
Open `.env` and add your keys:
```
ANTHROPIC_API_KEY=your-anthropic-key-here
VOYAGE_API_KEY=your-voyage-key-here
```

**4. Run the files**
```bash
# Verify your setup works
python3 prompt_and_eval/test.py

# Run a prompt against test cases (no scoring)
python3 prompt_and_eval/prompt_runner.py

# Scale-based evals (LLM-as-judge)
python3 prompt_and_eval/prompt_judge.py
python3 prompt_and_eval/prompt_judge_cot.py
python3 prompt_and_eval/prompt_comparison.py

# Other eval patterns
python3 prompt_and_eval/binary_eval.py
python3 prompt_and_eval/ordinal_eval.py
python3 prompt_and_eval/classification_eval.py
python3 prompt_and_eval/likert_eval.py
python3 prompt_and_eval/rouge_eval.py
python3 prompt_and_eval/cosine_similarity_eval.py
python3 prompt_and_eval/exact_match_eval.py

# RAG demos
python3 rag/rag_demo.py
python3 rag/semantic_search.py
```

## How It Works

### Prompt Eval (LLM-as-Judge)

**Step 1 — The Agent**
Claude is given a system prompt and responds to test inputs.

**Step 2 — The Judge**
A second Claude call evaluates the response on defined criteria (politeness, clarity, helpfulness, conciseness, etc).

**Step 3 — Compare & Iterate**
Prompts are scored and ranked. The winning prompt is the one that consistently scores highest across all test cases.

### Chain-of-Thought (CoT) Judge

The CoT version asks the judge to **reason through each criterion individually before scoring**. This produces more transparent, more accurate, and more honest evaluations — though it is slower and uses more tokens.

**Trade-offs:**
- ✅ More accurate and consistent scoring
- ✅ Transparent reasoning you can debug
- ❌ Slower response time
- ❌ Higher token cost

### Eight Eval Patterns

Different tasks call for different eval patterns:

- **Exact match** — strict string comparison, ideal for classification tasks
- **Binary** — LLM judge gives a yes/no verdict against a golden answer
- **Ordinal (1-5)** — ranked categories of quality
- **Likert (1-5)** — measures how strongly a response matches a target trait
- **Scale (1-10)** — broader range, good for overall quality
- **Classification** — verifies a response is compliant (no PHI leakage, etc)
- **ROUGE-L F1** — pure math, measures word overlap with a reference
- **Cosine similarity** — uses embeddings to measure semantic similarity across responses

LLM judges are flexible but cost money. Metric-based evals (ROUGE, cosine similarity, exact match) are free and instant but only measure what they're designed for. Real eval pipelines combine multiple patterns for a complete picture.

### RAG Demo

**Step 1 — Retrieval**
Load relevant content from `company_faq.txt`.

**Step 2 — Augmented**
Stuff the relevant content into the prompt as context.

**Step 3 — Generation**
Claude answers the user's question based on the provided context — and honestly says "I don't know" when the answer isn't in the FAQ.

### Semantic Search

The basic RAG demo sends the entire FAQ to Claude as context. That works for small documents but doesn't scale. Semantic search upgrades this:

**Step 1 — Chunk**
Split the FAQ into smaller sections.

**Step 2 — Embed**
Convert each chunk into a 1024-dimensional vector using Voyage AI's `voyage-3` model.

**Step 3 — Search**
Convert the user's question into a vector and find the chunks with the highest cosine similarity.

**Step 4 — Retrieve only the top matches**
Send just the most relevant chunks to Claude instead of the whole document — cheaper, faster, and scales to thousands of documents.

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

Both the baseline judge and the CoT judge produced the same final aggregate score of **8.2/10** — but the CoT judge surfaced individual weaknesses much more clearly. For example, one test case scored 6/10 with CoT because the judge broke down conciseness (4/10) separately from clarity (7/10), exposing over-formatting that the baseline judge had glossed over with a vague "slightly verbose" comment.

The takeaway: **CoT doesn't always change the score, but it always changes the quality of the evaluation.** It makes weaknesses visible and reasoning auditable — which matters far more than the final number when you're trying to improve a prompt.

This mirrors a key insight from the Constitutional AI paper:

> *"Both the SL and RL methods can leverage chain-of-thought style reasoning to improve the human-judged performance and transparency of AI decision making."*

See the full breakdown in [`prompt_and_eval/prompt_judge_results.md`](./prompt_and_eval/prompt_judge_results.md).

### RAG Demo

Claude correctly answered 3 questions using the FAQ as context and honestly admitted it didn't know the dress code (not in the FAQ) instead of making something up — exactly the "harmless but non-evasive" behavior the Anthropic Model Spec describes.

See the full breakdown in [`rag/rag_results.md`](./rag/rag_results.md).

### Semantic Search

The semantic search demo correctly matched each test question to the right FAQ chunk based on meaning — not keywords. For example, "How many vacation days do I get?" returned the **PTO Policy** chunk as the top match, even though neither the question nor the chunk shares the same word for time off.

This proves embeddings encode **meaning**, not vocabulary — which is exactly what makes them useful for retrieval at scale.

See the full breakdown in [`rag/semantic_search_results.md`](./rag/semantic_search_results.md).

## Key Insight

The judge has no memory of writing the response it evaluates. By giving Claude a different persona (evaluator vs. agent), it assesses the output neutrally — the same principle behind Constitutional AI and RLHF. Adding Chain-of-Thought reasoning to that judge makes the evaluation even more transparent and accurate, at the cost of speed and tokens. And by using embeddings — both for retrieval (semantic search) and measurement (consistency checks) — the same underlying tool powers two completely different kinds of intelligence.

## Built With

- [Anthropic API](https://docs.anthropic.com) — Claude
- [Voyage AI](https://www.voyageai.com/) — embeddings for semantic search
- [sentence-transformers](https://www.sbert.net/) — embeddings for consistency evals
- [rouge](https://pypi.org/project/rouge/) — ROUGE-L metric
- Python 3
- python-dotenv