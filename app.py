# BPE Structured Pricing Assistant - Version 4.0 (Hybrid Search)

# --- 📚 1. Install Requirements (if needed) ---
!pip install pymongo openai voyageai

# --- 🛠️ 2. Import Libraries ---
import os
import pymongo
import openai
import logging
from voyageai import Client as VoyageClient

# --- 🏗️ 3. Setup Logging ---
logging.basicConfig(level=logging.INFO)

# --- 🔐 4. Set Up API Keys and MongoDB URI ---
MONGO_URI = ""
OPENAI_KEY = ""
VOYAGE_KEY = ""

# --- 📦 5. Initialize Clients ---
client = pymongo.MongoClient(MONGO_URI)
db = client.bpe_demo_structured
drug_pricing = db.drug_pricing

openai.api_key = OPENAI_KEY
voyage_client = VoyageClient(api_key=VOYAGE_KEY)

# --- 🧱 6. Example Document Structure ---
example_doc = {
    "drug": "Lipitor",
    "generic": "Atorvastatin",
    "location": "New York City",
    "pharmacy": "Walmart",
    "price": 12,
    "supply_days": 30,
    "customer_id": "acmehealth123",
    "last_updated": {"$date": "2024-04-26T00:00:00Z"}
}

# --- 🔍 7. Structured Pricing Lookup Function ---
def find_cheapest_drug(drug_name, city_name):
    query = {
        "drug": {"$regex": drug_name, "$options": "i"},
        "location": {"$regex": city_name, "$options": "i"}
    }
    result = drug_pricing.find(query).sort("price", 1).limit(1)
    return list(result)

# --- 🧠 8. Vector Search + GPT-4 Fallback ---
def search_documents(query, customer=None, top_k=3):
    try:
        response = voyage_client.embed([query], model="voyage-lite-02-instruct")
        query_vector = response.embeddings[0]

        pipeline = [
            {
                "$vectorSearch": {
                    "queryVector": query_vector,
                    "path": "embedding",
                    "numCandidates": 50,
                    "limit": top_k,
                    "index": "drug_pricing"
                }
            }
        ]

        if customer:
            pipeline.append({"$match": {"customer": customer}})

        return list(db.customer_pricing.aggregate(pipeline))
    except Exception as e:
        logging.error(f"Search error: {e}")
        return []

# --- ✨ 9. GPT-4 Recommendation Generation ---
def generate_recommendation(user_query, customer=None):
    results = search_documents(user_query, customer)
    if not results:
        return "No relevant pricing information found."

    context = "\n".join(
        f"- {doc.get('drug', 'Unknown Drug')} at {doc.get('pharmacy', 'Unknown Pharmacy')} in {doc.get('location', 'Unknown Location')} for ${doc.get('price', 'N/A')}"
        for doc in results
    )

    prompt = f"""
    You are a helpful assistant in a pharmaceutical pricing recommendation system.
    The user asked: \"{user_query}\"
    Here is relevant context from internal pricing records:
    {context}
    Please generate a concise and helpful pricing recommendation.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful pricing assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        logging.error(f"OpenAI generation error: {e}")
        return "An error occurred while generating a recommendation."

# --- 🖥️ 10. Interactive CLI Simulation ---
def run_cli():
    print("\n💊 BPE Pricing Assistant (Structured Data Edition)\n(Type 'exit' to quit.)\n")
    while True:
        user_input = input("🧑\u200d⚕️ You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        if not user_input:
            print("⚠️ Please enter a valid query.")
            continue

        # Quick hardcoded matching examples
        matched = False
        if "metformin" in user_input.lower() and "houston" in user_input.lower():
            results = find_cheapest_drug("Metformin", "Houston")
            matched = True
        elif "lipitor" in user_input.lower() and "chicago" in user_input.lower():
            results = find_cheapest_drug("Lipitor", "Chicago")
            matched = True
        elif "atorvastatin" in user_input.lower() and "new york" in user_input.lower():
            results = find_cheapest_drug("Atorvastatin", "New York City")
            matched = True
        elif "ozempic" in user_input.lower() and "los angeles" in user_input.lower():
            results = find_cheapest_drug("Ozempic", "Los Angeles")
            matched = True
        elif "trulicity" in user_input.lower() and "atlanta" in user_input.lower():
            results = find_cheapest_drug("Trulicity", "Atlanta")
            matched = True
        else:
            results = []

        if matched and results:
            doc = results[0]
            print(f"\n🤖 BPE Assistant:\n{doc['drug']} is available at {doc['pharmacy']} in {doc['location']} for ${doc['price']}.\n")
        else:
            answer = generate_recommendation(user_input)
            print(f"\n🤖 BPE Assistant:\n{answer}\n")

# --- 🚀 11. Run the Assistant ---
run_cli()
