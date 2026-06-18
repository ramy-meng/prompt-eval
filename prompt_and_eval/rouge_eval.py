from rouge import Rouge
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


# Articles with reference summaries to compare against
articles = [
    {
        "text": "In a groundbreaking study, researchers at MIT have discovered a new class of antibiotics effective against drug-resistant bacteria. The research team, led by Dr. Sarah Chen, used machine learning models to identify compounds that target previously unexplored bacterial pathways. Early trials show the antibiotics are effective against several strains that have been resistant to existing treatments for decades. The discovery could mark a turning point in the global fight against antibiotic resistance, which the World Health Organization has called one of the most urgent threats to public health.",
        "summary": "MIT scientists discover a new antibiotic effective against drug-resistant bacteria, marking a major breakthrough in fighting antibiotic resistance.",
    },
    {
        "text": "Jane Doe, a local hero, made headlines last week for saving three children from a burning building in downtown Springfield. In city hall news, the proposed budget for the next fiscal year has sparked heated debate among council members, with disagreements over education funding and infrastructure spending. Meanwhile, meteorologists predict an unusually warm winter, with temperatures expected to remain above seasonal averages through February.",
        "summary": "Community celebrates local hero Jane Doe while city grapples with budget issues and forecasters predict a warm winter.",
    },  # Edge case: Multi-topic
    {
        "text": "You won't believe what this celebrity did! Famous actor John Smith, known for his roles in blockbuster films, has been quietly funding scholarships for underprivileged students for over a decade. His extensive charity work, which has remained largely out of the spotlight, has helped more than 500 students pursue higher education. Smith has also founded a nonprofit organization focused on literacy programs in low-income communities.",
        "summary": "Celebrity John Smith's extensive charity work funding scholarships and literacy programs surprises fans.",
    },  # Edge case: Misleading clickbait title
]


# Get Claude's summary of an article
def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# Evaluate using ROUGE-L F1 score — pure math, no LLM judge needed
def evaluate_rouge_l(model_output, true_summary):
    rouge = Rouge()
    scores = rouge.get_scores(model_output, true_summary)
    return scores[0]["rouge-l"]["f"]  # ROUGE-L F1 score (0.0 to 1.0)


# Run all evals and log to file
with open("rouge_eval_results.md", "w") as log:
    log.write("# ROUGE-L Eval Results — Summarization Quality\n\n")
    log.write("Results from running `rouge_eval.py` — a **metric-based eval** that compares Claude's summaries against reference summaries using ROUGE-L F1 (Longest Common Subsequence). Unlike LLM-as-judge evals, this is pure math: no API calls for grading, no subjectivity, deterministic results.\n\n")
    log.write("---\n\n")

    scores = []

    for i, article in enumerate(articles, 1):
        text = article["text"]
        reference_summary = article["summary"]

        # Get Claude's summary
        output = get_completion(
            f"Summarize this article in 1-2 sentences:\n\n{text}"
        )

        # Score with ROUGE-L
        score = evaluate_rouge_l(output, reference_summary)
        scores.append(score)

        # Print to terminal
        print(f"\n=== ARTICLE {i} ===")
        print(f"Reference Summary: {reference_summary}")
        print(f"Claude's Summary: {output}")
        print(f"ROUGE-L F1 Score: {score:.3f}")
        print("-" * 60)

        # Write to file
        log.write(f"## Article {i}\n\n")
        log.write(f"**Original Article:**\n\n{text}\n\n")
        log.write(f"**Reference Summary:** {reference_summary}\n\n")
        log.write(f"**Claude's Summary:** {output}\n\n")
        log.write(f"**ROUGE-L F1 Score:** {score:.3f}\n\n")
        log.write("---\n\n")

    # Final average
    average_score = sum(scores) / len(scores)
    print(f"\n{'='*60}")
    print(f"✅ AVERAGE ROUGE-L F1 SCORE: {average_score:.3f}")
    print(f"{'='*60}")

    log.write(f"## ✅ Average ROUGE-L F1 Score: {average_score:.3f}\n\n")
    log.write("## What ROUGE-L Measures\n\n")
    log.write("ROUGE-L counts how much the **longest common subsequence** of words overlaps between Claude's summary and the reference summary. It rewards summaries that preserve the same content in roughly the same order, normalized to a score between 0.0 (no overlap) and 1.0 (identical text).\n\n")
    log.write("## Key Takeaway\n\n")
    log.write("Metric-based evals like ROUGE are **fast, free, and deterministic** — but they only measure word overlap, not meaning. Two summaries can mean the same thing while scoring low (different vocabulary) or share lots of words while meaning different things.\n\n")
    log.write("In production eval pipelines, ROUGE is usually combined with LLM-as-judge evals:\n")
    log.write("- **ROUGE** → cheap, fast first-pass filter\n")
    log.write("- **LLM judge** → expensive but captures meaning and quality\n\n")
    log.write("This combo is how big AI labs evaluate summarization, translation, and structured output at scale.\n")

print("\n✅ Results saved to rouge_eval_results.md")