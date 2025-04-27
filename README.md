### BPE Structured Pricing Assistant - Version 4.0 (Hybrid Search) 💊 

This project demonstrates a hybrid approach to pharmaceutical pricing assistance by combining structured MongoDB lookups with AI fallback search using vector embeddings and GPT-4.
This system is designed as a prototype — in production, pricing data would likely come from automated ingestion pipelines or enterprise pricing databases.


 🛠️ How It Works

1. **Structured Data First:**  
   - Pricing records (drug, pharmacy, location, price, etc.) are inserted into MongoDB (`drug_pricing` collection).
   - When a user asks a question, the assistant first tries to **find exact matches** by drug name and city using MongoDB queries.
<br>
2. **Vector Search + GPT-4 Fallback:**  
   - If no exact pricing match is found, the system falls back to **vector search** (Voyage AI embeddings) and **GPT-4** to generate helpful recommendations based on semantic similarity.


 📦 What's Included

- `BPE_Structured_v4.ipynb`:  
  Full Jupyter Notebook (Colab-ready) with:
  - MongoDB setup
  - Pricing document insertion
  - Search functions
  - Hybrid CLI assistant
- `README.md` (this file)

---

 🚀 How to Run It (Colab or Local Jupyter)

1. **Clone or download** this repository / Gist.

2. **Open `BPE_Structured_v4.ipynb`** in:
   - Google Colab (recommended for easiest setup)
   - or Jupyter Notebook locally.

3. **Install requirements** (Colab will auto-prompt if missing):
   ```bash
   !pip install pymongo openai voyageai
