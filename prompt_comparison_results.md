# Prompt Comparison Results
 
This document shows the results of running three different system prompts through an automated eval system built with the Anthropic API. Each prompt was tested against 5 customer support scenarios and scored by Claude acting as an impartial judge.
 
To reproduce these results, run `prompt_comparison.py` in this repo.
 
---
 
## How It Works
 
1. Each prompt is given to Claude as a system prompt
2. Claude responds to 5 different customer support messages
3. A second Claude instance acts as a judge and scores each response 1-10
4. Scores are averaged to produce a final rating per prompt
---
 
## The Prompts
 
**Prompt A — Original**
```
You are a helpful customer support agent.
Answer questions clearly and concisely.
Always be polite and professional.
```
 
**Prompt B — Empathetic**
```
You are a warm and empathetic customer support agent.
Always acknowledge the customer's feelings first before solving their problem.
Use simple language, avoid jargon, and keep responses brief.
If you don't know something, be honest and direct them to the right place.
```
 
**Prompt C — Conversational**
```
You are a friendly customer support agent.
Keep responses short and conversational — no bullet points or headers unless absolutely necessary.
Acknowledge the customer's feelings first, then solve the problem in plain language.
If a customer is angry or frustrated, skip emojis and be calm and direct.
If you don't know something, be honest and point them in the right direction.
```
 
---
 
## Test Cases
 
The same 5 messages were used to test all three prompts:
 
1. "My order hasn't arrived yet, what should I do?"
2. "I want a refund NOW, this is ridiculous!"
3. "What's your return policy?"
4. "You guys are the worst company ever."
5. "Can I change my delivery address?"
These were chosen to cover a range of scenarios: a standard question, an angry customer, a policy question, an abusive message, and a simple request.
 
---
 
## Results
 
| Prompt | Description | Final Score |
|--------|-------------|-------------|
| Prompt A | Original — polite and professional | 8.2/10 |
| Prompt B | Empathetic — acknowledge feelings first | 8.4/10 |
| **Prompt C** | **Conversational — no markdown, no emojis when angry** | **9.0/10** |
 
🏆 **Winner: Prompt C (9.0/10)**
 
---
 
## Detailed Scores
 
### Prompt A — 8.2/10
 
| # | User Message | Score | Judge Feedback |
|---|-------------|-------|----------------|
| 1 | My order hasn't arrived yet, what should I do? | 9/10 | Warm and helpful with clear steps, slightly longer than necessary |
| 2 | I want a refund NOW, this is ridiculous! | 9/10 | Empathetic and actionable, closing emoji feels formulaic for a frustrated customer |
| 3 | What's your return policy? | 7/10 | Overly formatted and disclaimer undermines helpfulness |
| 4 | You guys are the worst company ever. | 8/10 | Warm and inviting, could acknowledge frustration more directly |
| 5 | Can I change my delivery address? | 8/10 | Helpful but over-formatted with headers for a simple question |
 
### Prompt B — 8.4/10
 
| # | User Message | Score | Judge Feedback |
|---|-------------|-------|----------------|
| 1 | My order hasn't arrived yet, what should I do? | 9/10 | Warm and helpful, emoji usage slightly excessive |
| 2 | I want a refund NOW, this is ridiculous! | 8/10 | Empathetic but "totally valid" feels informal in a tense situation |
| 3 | What's your return policy? | 8/10 | Honest and helpful, slightly over-explained |
| 4 | You guys are the worst company ever. | 9/10 | Warm and de-escalating, emoji may feel informal in some brand contexts |
| 5 | Can I change my delivery address? | 8/10 | Clear and helpful, emotionally inflated for a simple question |
 
### Prompt C — 9.0/10 🏆
 
| # | User Message | Score | Judge Feedback |
|---|-------------|-------|----------------|
| 1 | My order hasn't arrived yet, what should I do? | 9/10 | Warm and actionable, proactively invites further help |
| 2 | I want a refund NOW, this is ridiculous! | 9/10 | Calm, de-escalating, immediately requests info needed to resolve |
| 3 | What's your return policy? | 9/10 | Clear and helpful while honestly acknowledging limitations |
| 4 | You guys are the worst company ever. | 9/10 | Empathetic and efficient, no defensiveness |
| 5 | Can I change my delivery address? | 9/10 | Covers both scenarios clearly, invites customer to share more |
 
---
 
## Key Takeaways
 
**Over-formatting hurts scores.** Headers and bullet points for simple questions feel like documentation, not a real conversation. The judge consistently flagged this in Prompts A and B.
 
**Emojis backfire with angry customers.** Prompt C explicitly avoids them when frustration is detected. Prompts A and B both lost points for using emojis in tense situations.
 
**Conversational tone wins.** Plain language outperforms structured responses for support interactions. Explaining the *why* behind instructions (e.g. "skip emojis when angry") produces better behavior than rules alone.
 
**LLM judges have variance.** Running the same eval multiple times produces slightly different scores. For reliable results, run at least 3 times and average the scores.
 
---
 
## What's Next
 
- Add more test cases covering edge cases (e.g. multilingual customers, technical questions)
- Test Prompt D with even tighter instructions based on judge feedback
- Experiment with different judge criteria to see how scoring changes