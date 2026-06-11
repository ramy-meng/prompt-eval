import anthropic
import os
from dotenv import load_dotenv
import voyageai

load_dotenv()

# We'll use Voyage AI for embeddings since Anthropic recommends them
# Get a free API key at https://www.voyageai.com/
vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

# Step 1: Break the FAQ into chunks (each section is one chunk)
chunks = [
    "PTO Policy: All full-time employees receive 20 days of paid time off per year. PTO must be requested at least 2 weeks in advance through the HR portal. Unused PTO does not roll over to the next year.",
    "Remote Work Policy: Employees can work remotely up to 3 days per week. Tuesdays and Thursdays are required in-office days for all team collaboration. Exceptions require manager approval.",
    "Health Benefits: We offer comprehensive health insurance covering medical, dental, and vision. Coverage begins on the first day of employment. The company covers 80% of the premium and employees cover 20%.",
    "Expense Reimbursement: Submit expense reports through the Expensify app within 30 days of purchase. Reimbursements are processed every Friday. Receipts are required for any expense over $25.",
    "Office Hours: Standard office hours are 9 AM to 5 PM. Core collaboration hours are 10 AM to 3 PM during which all team members should be available."
]

# Step 2: Embed all the chunks (turn them into vectors)
print("Embedding chunks...")
chunk_embeddings = vo.embed(chunks, model="voyage-3").embeddings
print(f"✅ Created {len(chunk_embeddings)} embeddings, each with {len(chunk_embeddings[0])} dimensions\n")

# Step 3: Cosine similarity function
def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = sum(x ** 2 for x in a) ** 0.5
    magnitude_b = sum(x ** 2 for x in b) ** 0.5
    return dot_product / (magnitude_a * magnitude_b)

# Step 4: Search function — find the most relevant chunk
def find_relevant_chunk(question):
    question_embedding = vo.embed([question], model="voyage-3").embeddings[0]
    
    # Compute similarity for each chunk
    scores = []
    for i, chunk_embedding in enumerate(chunk_embeddings):
        score = cosine_similarity(question_embedding, chunk_embedding)
        scores.append((score, chunks[i]))
    
    # Sort by highest similarity
    scores.sort(reverse=True)
    return scores

# Step 5: Test it
questions = [
    "How many vacation days do I get?",       # Should match PTO chunk
    "Can I work from home on Tuesday?",       # Should match Remote Work chunk
    "Where do I submit my receipts?",         # Should match Expense chunk
]

for q in questions:
    print(f"❓ Question: {q}")
    results = find_relevant_chunk(q)
    time.sleep(25)  # Wait 25 seconds to stay under Voyage's 3 RPM free tier limit
    
    print("Top 3 most relevant chunks:")
    for score, chunk in results[:3]:
        print(f"  [{score:.3f}] {chunk[:80]}...")
    print("-" * 60)