import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

# STEP 1: Load the knowledge base (your "documents")
with open("company_faq.txt", "r") as f:
    knowledge_base = f.read()

# STEP 2: Simple retrieval — find the relevant section
def retrieve_context(question, knowledge):
    """
    For simplicity, we send the whole FAQ to Claude.
    In a real RAG system, you'd use a vector database to find only the relevant section.
    """
    return knowledge

# STEP 3: Ask Claude with the retrieved context
def ask_with_rag(question):
    context = retrieve_context(question, knowledge_base)
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"""Based on the following company FAQ, answer the user's question.
If the answer isn't in the FAQ, say so honestly.

COMPANY FAQ:
{context}

QUESTION: {question}"""
            }
        ]
    )
    return response.content[0].text

# STEP 4: Test it with different questions
questions = [
    "How many PTO days do I get?",
    "Can I work remotely on Tuesday?",
    "What's the dress code?",  # Not in FAQ — let's see if Claude is honest
    "When do I get reimbursed for expenses?"
]

for q in questions:
    print(f"\n❓ Question: {q}")
    print(f"💬 Answer: {ask_with_rag(q)}")
    print("-" * 60)