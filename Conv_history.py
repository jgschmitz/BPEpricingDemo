from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_voyageai import VoyageAIEmbeddings

# 1. Setup the Vector Store abstraction
vector_store = MongoDBAtlasVectorSearch(
    collection=db.customer_pricing,
    embedding=VoyageAIEmbeddings(api_key=VOYAGE_KEY, model="voyage-lite-02-instruct"),
    index_name="drug_pricing"
)

# 2. Use it as a Retriever with pre-filtering
def search_with_langchain(query, customer_id):
    retriever = vector_store.as_retriever(
        search_kwargs={'pre_filter': {'customer_id': customer_id}}
    )
    return retriever.get_relevant_documents(query)
