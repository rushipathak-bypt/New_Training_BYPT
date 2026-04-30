import fitz  # PyMuPDF
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# 📄 Extract text from PDF
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 🧩 Chunking with overlap (better context)
def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        
    return chunks

data = []

# Load PDFs
for file in os.listdir("data"):
    if file.endswith(".pdf"):
        text = extract_text(f"data/{file}")
        chunks = chunk_text(text)

        for chunk in chunks:
            data.append({
                "text": chunk,
                "source": file
            })

print(f"Total chunks: {len(data)}")

# 🔢 Embeddings
texts = [d["text"] for d in data]
embeddings = model.encode(texts)

# 📦 FAISS index
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# 💾 Save
os.makedirs("faiss_index", exist_ok=True)

faiss.write_index(index, "faiss_index/index.bin")

with open("faiss_index/data.pkl", "wb") as f:
    pickle.dump(data, f)

print("✅ Ingestion complete")