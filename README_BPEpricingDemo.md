# BPE Pricing Demo

A lightweight demo of a **hybrid pharmaceutical pricing assistant** that combines deterministic MongoDB lookups with semantic search and GPT-generated recommendations.

The demo is designed to show how an assistant can answer pricing questions in two stages:

1. **Structured lookup first** — query known pricing records by drug and location.
2. **Semantic fallback second** — use Voyage AI embeddings, MongoDB Atlas Vector Search, and GPT to generate a helpful response when an exact match is not available.

> This repository is a prototype for demonstration purposes. It is not intended for production use, medical advice, or real-world pharmacy pricing decisions without additional validation, data governance, security, and compliance controls.

---

## What this demo shows

- How to store and query structured pharmacy pricing records in MongoDB.
- How to prioritize exact, explainable database matches before using generative AI.
- How to use embeddings and vector search as a fallback for less exact user questions.
- How to generate concise natural-language recommendations from retrieved pricing context.
- How to run a simple command-line pricing assistant loop.

---

## Architecture

```text
User question
   |
   v
CLI assistant
   |
   +--> Structured MongoDB lookup
   |       - drug name regex match
   |       - location regex match
   |       - sort by lowest price
   |
   +--> If no structured match
           |
           v
       Voyage AI embedding
           |
           v
       MongoDB Atlas Vector Search
           |
           v
       GPT recommendation
```

The intended behavior is simple: use the most reliable structured data path first, then fall back to semantic retrieval and generation only when needed.

---

## Repository contents

| File | Description |
| --- | --- |
| `app.py` | Main demo script. Installs dependencies, initializes clients, defines lookup/search functions, and starts an interactive CLI assistant. |
| `README.md` | Project documentation. |

---

## Prerequisites

You will need:

- Python 3.9+
- A MongoDB Atlas cluster or accessible MongoDB deployment
- A MongoDB Atlas Vector Search index for semantic search
- An OpenAI API key
- A Voyage AI API key

Python packages used by the demo:

```bash
pip install pymongo openai voyageai
```

---

## Configuration

Open `app.py` and set the following values:

```python
MONGO_URI = "<your MongoDB connection string>"
OPENAI_KEY = "<your OpenAI API key>"
VOYAGE_KEY = "<your Voyage AI API key>"
```

The script initializes MongoDB like this:

```python
client = pymongo.MongoClient(MONGO_URI)
db = client.bpe_demo_structured
drug_pricing = db.drug_pricing
```

The structured lookup reads from:

```text
bpe_demo_structured.drug_pricing
```

The vector search function currently aggregates from:

```text
bpe_demo_structured.customer_pricing
```

For the smoothest demo experience, make sure your test data and vector-search collection names are aligned with the code you intend to run.

---

## Example pricing document

The demo uses pricing records shaped like this:

```json
{
  "drug": "Lipitor",
  "generic": "Atorvastatin",
  "location": "New York City",
  "pharmacy": "Walmart",
  "price": 12,
  "supply_days": 30,
  "customer_id": "acmehealth123",
  "last_updated": {
    "$date": "2024-04-26T00:00:00Z"
  }
}
```

For vector search, each searchable document should also include an `embedding` field that matches the vector index configuration.

---

## MongoDB Atlas Vector Search index

The demo expects a vector index named:

```text
drug_pricing
```

The vector search pipeline uses:

```python
"$vectorSearch": {
    "queryVector": query_vector,
    "path": "embedding",
    "numCandidates": 50,
    "limit": top_k,
    "index": "drug_pricing"
}
```

Your Atlas Vector Search index should therefore include an embedding field named `embedding`.

A representative index definition may look like this, adjusted for the actual embedding dimensions produced by your selected Voyage model:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1024,
      "similarity": "cosine"
    }
  ]
}
```

Check the Voyage AI model documentation for the exact embedding dimension of the model you use.

---

## Running the demo

### Option 1: Google Colab or Jupyter

The current script is notebook-friendly because it includes a notebook-style install command:

```python
!pip install pymongo openai voyageai
```

Open `app.py` in a notebook environment, configure your keys, and run the cells or script.

### Option 2: Local Python

If running as a normal Python script, remove or comment out the notebook install line:

```python
!pip install pymongo openai voyageai
```

Then install dependencies from your terminal:

```bash
pip install pymongo openai voyageai
```

Run:

```bash
python app.py
```

---

## Example prompts

The CLI includes a few hardcoded routing examples that attempt structured lookup first:

```text
What is the cheapest Metformin in Houston?
How much is Lipitor in Chicago?
Find Atorvastatin in New York.
What is the price of Ozempic in Los Angeles?
Where can I get Trulicity in Atlanta?
```

If the query does not match one of the structured examples, the assistant falls back to semantic search and GPT-based recommendation generation.

---

## How the code works

### 1. Structured lookup

`find_cheapest_drug()` searches MongoDB by drug and city using case-insensitive regex matching, sorts by price ascending, and returns the lowest-priced match.

```python
def find_cheapest_drug(drug_name, city_name):
    query = {
        "drug": {"$regex": drug_name, "$options": "i"},
        "location": {"$regex": city_name, "$options": "i"}
    }
    result = drug_pricing.find(query).sort("price", 1).limit(1)
    return list(result)
```

### 2. Semantic fallback

`search_documents()` embeds the user query with Voyage AI and sends the vector to MongoDB Atlas Vector Search.

### 3. Recommendation generation

`generate_recommendation()` formats the retrieved pricing records as context and asks GPT to produce a concise recommendation.

### 4. Interactive loop

`run_cli()` starts a terminal-style assistant session. Type `exit` or `quit` to end the session.

---

## Important implementation notes

- The demo currently uses placeholder secrets in the source file. For public repositories, prefer environment variables instead of hardcoding credentials.
- The script uses older OpenAI Python SDK syntax: `openai.ChatCompletion.create(...)`. If you are using a newer OpenAI SDK version, you may need to update the client initialization and chat completion call.
- The structured lookup uses `drug_pricing`, while vector search uses `customer_pricing`. Confirm whether you want one collection or two before presenting the demo.
- The optional `customer` filter checks for a field named `customer`, while the example document uses `customer_id`. Align the field name if customer-specific filtering is part of the demo.
- Pricing data in this repository should be treated as sample data unless connected to a governed pricing source.

---

## Suggested production improvements

Before adapting this pattern for real use, consider adding:

- Secure secret management using environment variables or a secrets manager.
- Automated data ingestion and validation.
- Data freshness checks and clear `last_updated` handling.
- Role-based access control and customer-level filtering.
- Audit logging for pricing recommendations.
- Automated tests for exact-match and fallback behavior.
- Error handling for unavailable API providers.
- A web UI or API layer instead of only a CLI.
- Guardrails that distinguish pricing assistance from medical advice.

---

## Security and compliance reminder

This demo handles pharmaceutical pricing-style data. A production implementation may involve sensitive commercial, customer, or healthcare-adjacent information. Review applicable security, privacy, and compliance requirements before using real data.

Do not commit real API keys, credentials, customer records, or regulated data to this repository.

---

## License

No license is currently specified in this README. Add a license file if you want others to use, modify, or distribute this demo.

---

## Maintainer notes

This README is written for a public demo repository. It intentionally explains the architecture, setup, limitations, and likely next steps so reviewers can understand the value of the demo quickly.
