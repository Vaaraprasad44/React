from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Load and Prepare Data -----------------
df = pd.read_csv("c:/Users/membe/OneDrive/Desktop/Mr.cooper/hackathon/backend/imdb_top_1000.csv")
df.dropna(subset=["Series_Title", "Overview"], inplace=True)
df.reset_index(drop=True, inplace=True)

# Initialize sentence-transformer and FAISS
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Encoding movie overviews...")
descriptions = df["Overview"].tolist()
embeddings = model.encode(descriptions, show_progress_bar=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))
print("FAISS index created.")

# ----------------- Pydantic Models -----------------
class SearchRequest(BaseModel):
    query: str
    num_results: int = 10

class RecommendRequest(BaseModel):
    movie_title: str
    num_results: int = 10

# ----------------- Routes -----------------

@app.get("/")
def home():
    return {"message": "🎬 Welcome to the Movie Recommender API!"}

@app.post("/api/search")
def search_movies(request: SearchRequest):
    query_vec = model.encode([request.query])
    D, I = index.search(np.array(query_vec), request.num_results)
    results = df.iloc[I[0]][["Series_Title", "Overview"]].rename(
        columns={"Series_Title": "title", "Overview": "description"}
    ).to_dict(orient="records")
    return {"success": True, "query": request.query, "results": results}

@app.post("/api/recommend")
def recommend_movies(request: RecommendRequest):
    match = df[df["Series_Title"].str.lower() == request.movie_title.lower()]
    if match.empty:
        return {"success": False, "error": f"Movie '{request.movie_title}' not found"}
    idx = match.index[0]
    movie_vec = np.array([embeddings[idx]])
    D, I = index.search(movie_vec, request.num_results + 1)
    indices = I[0][1:]  # skip self
    results = df.iloc[indices][["Series_Title", "Overview"]].rename(
        columns={"Series_Title": "title", "Overview": "description"}
    ).to_dict(orient="records")
    return {"success": True, "based_on": request.movie_title, "results": results}

@app.get("/api/movies")
def get_all_movies():
    movies = df[["Series_Title", "Overview"]].rename(
        columns={"Series_Title": "title", "Overview": "description"}
    ).to_dict(orient="records")
    return {"success": True, "count": len(movies), "movies": movies}

@app.get("/api/stats")
def get_stats():
    return {
        "success": True,
        "stats": {
            "total_movies": len(df),
            "embedding_dim": embeddings.shape[1]
        }
    }

# uvicorn main:app --reload or uvicorn file_name:app --reload