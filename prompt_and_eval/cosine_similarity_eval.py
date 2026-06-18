from sentence_transformers import SentenceTransformer
import numpy as np
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


# FAQ variations — same underlying question phrased differently
faq_variations = [
    {
        "topic": "Return policy",
        "questions": [
            "What's your return policy?",
            "How can I return an item?",
            "Wut's yur retrn polcy?",
        ],
    },  # Edge case: Typos
    {
        "topic": "Return policy with rambling",
        "questions": [
            "I bought something last week, and it's not really what I expected, so I was wondering if maybe I could possibly return it?",
            "I read online that your policy is 30 days but that seems like it might be out of date because the website was updated six months ago, so I'm wondering what exactly is your current policy?",
        ],
    },  # Edge case: Long, rambling question
    {
        "topic": "Return policy with irrelevant info",
        "questions": [
            "I'm Jane's cousin, and she said you guys have great customer service. Can I return this?",
            "Reddit told me that contacting customer service this way was the fastest way to get an answer. I hope they're right! What is the return window for a jacket?",
        ],
    },  # Edge case: Irrelevant info
]


# Get Claude's response
def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# Load embedding model once (reusable across all evals)
print("Loading sentence transformer model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded\n")


# Evaluate consistency using pairwise cosine similarity
def evaluate_cosine_similarity(outputs):
    embeddings = embedding_model.encode(outputs)
    norms = np.linalg.norm(embeddings, axis=1)
    cosine_similarities = np.dot(embeddings, embeddings.T) / np.outer(norms, norms)

    # Average of off-diagonal elements (skip self-similarity which is always 1.0)
    n = len(outputs)
    total = cosine_similarities.sum() - n  # subtract the diagonal (n self-similarities of 1.0)
    pairs = n * (n - 1)
    return total / pairs if pairs > 0 else 0


# Run all evals and log to file
with open("cosine_similarity_eval_results.md", "w") as log:
    log.write("# Cosine Similarity Eval Results — Consistency Testing\n\n")
    log.write("Results from running `cosine_similarity_eval.py` — a **metric-based consistency eval** that uses embeddings and cosine similarity to measure whether Claude gives semantically similar answers when the same question is phrased in different ways.\n\n")
    log.write("---\n\n")

    overall_scores = []

    for i, faq in enumerate(faq_variations, 1):
        topic = faq["topic"]
        questions = faq["questions"]

        # Get Claude's response to each variation
        outputs = [get_completion(question) for question in questions]

        # Score consistency
        similarity_score = evaluate_cosine_similarity(outputs)
        overall_scores.append(similarity_score)

        # Print to terminal
        print(f"\n=== FAQ {i}: {topic} ===")
        for j, (q, o) in enumerate(zip(questions, outputs), 1):
            print(f"Q{j}: {q}")
            print(f"A{j}: {o[:150]}...")
        print(f"Consistency Score: {similarity_score * 100:.1f}%")
        print("-" * 60)

        # Write to file
        log.write(f"## FAQ {i}: {topic}\n\n")
        for j, (q, o) in enumerate(zip(questions, outputs), 1):
            log.write(f"### Variation {j}\n\n")
            log.write(f"**Question:** {q}\n\n")
            log.write(f"**Claude's Answer:** {o}\n\n")
        log.write(f"**Consistency Score:** {similarity_score * 100:.1f}%\n\n")
        log.write("---\n\n")

    # Final average
    avg_consistency = sum(overall_scores) / len(overall_scores)
    print(f"\n{'='*60}")
    print(f"✅ AVERAGE FAQ CONSISTENCY SCORE: {avg_consistency * 100:.1f}%")
    print(f"{'='*60}")

    log.write(f"## ✅ Average FAQ Consistency Score: {avg_consistency * 100:.1f}%\n\n")
    log.write("## How It Works\n\n")
    log.write("1. The same underlying question is phrased multiple ways (typos, rambling, irrelevant info, etc).\n")
    log.write("2. Each variation is sent to Claude.\n")
    log.write("3. All responses are converted to embeddings (vectors that represent meaning).\n")
    log.write("4. Pairwise cosine similarity is calculated across all responses.\n")
    log.write("5. The average similarity becomes the consistency score — `1.0` means all responses are semantically identical, `0.0` means they're unrelated.\n\n")
    log.write("## Key Takeaway\n\n")
    log.write("Embeddings aren't only useful for retrieval — they're also a powerful **evaluation tool**. Here they're used to detect whether Claude is giving inconsistent answers depending on how a question is phrased, which is critical for FAQ bots and customer support systems.\n\n")
    log.write("This connects directly to the semantic search demo in `rag/semantic_search.py`. Same underlying tool (embeddings), totally different purpose:\n\n")
    log.write("- **Retrieval (semantic search)** → find the most similar chunk to a query\n")
    log.write("- **Evaluation (consistency check)** → measure how similar multiple responses are to each other\n")

print("\n✅ Results saved to cosine_similarity_eval_results.md")