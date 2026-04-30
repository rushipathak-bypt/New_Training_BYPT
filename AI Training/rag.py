import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index("faiss_index/index.bin")

# Load data (text + metadata)
with open("faiss_index/data.pkl", "rb") as f:
    data = pickle.load(f)

def retrieve(query, k=7):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)

    results = [data[i] for i in indices[0]]
    return results