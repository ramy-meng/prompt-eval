# RAG Demo Results

Results from running `rag_demo.py` — Claude answering questions using the company FAQ as context.

---

## ❓ How many PTO days do I get?

Based on our company FAQ, as a **full-time employee** you receive **20 days of paid time off per year**.

A couple of important things to keep in mind:
- PTO must be **requested at least 2 weeks in advance** through the HR portal
- **Unused PTO does not roll over** to the next year, so make sure to use it before year-end!

---

## ❓ Can I work remotely on Tuesday?

Based on the company's **Remote Work Policy**, **no** — Tuesday is one of the two **required in-office days** (along with Thursday) designated for team collaboration.

However, there is an exception process available: you would need to obtain **manager approval** if you require an exception to this rule.

---

## ❓ What's the dress code?

The company FAQ doesn't include any information about a **dress code policy**. I'd recommend reaching out to your **HR department** or **manager** directly to get clarification on dress code expectations. They'll be able to give you the most accurate and up-to-date information.

---

## ❓ When do I get reimbursed for expenses?

## Expense Reimbursements

Based on our company FAQ, here's what you need to know about getting reimbursed:

- **Reimbursements are processed every Friday**
- To ensure payment, you'll need to **submit your expense report through the Expensify app within 30 days of the purchase**
- Don't forget to include **receipts for any expense over $25**, otherwise your reimbursement could be delayed or denied

So your best bet is to submit your expenses as soon as possible to make sure they're processed in time for the next Friday payout!

---

## Key Takeaway

The RAG system worked correctly across all 4 questions — including the dress code question that wasn't in the FAQ. Claude honestly said it didn't have that information and pointed to HR instead of making something up. This is the "harmless but non-evasive" behavior the Constitutional AI paper describes in action.