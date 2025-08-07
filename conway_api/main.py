# conway_api/main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from conway import run_until_stable

app = FastAPI(
    title="Monument AI Conway Service",
    description="Simulates Conway’s Game of Life seeded with ASCII binary of a word",
    version="1.0.0"
)

# Enable CORS (modify origins for production deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationResult(BaseModel):
    generations: int
    score: int
    state: str

@app.get("/simulate", response_model=SimulationResult)
def simulate(word: str = Query(..., min_length=1, description="Seed word for Conway grid")):
    """
    Simulates Conway's Game of Life using ASCII binary of the word as seed.
    Returns generation count, score, and final state.
    """
    if not word.isascii():
        raise HTTPException(status_code=400, detail="Word must contain only ASCII characters")

    result = run_until_stable(seed_word=word.lower())
    return SimulationResult(**result)

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Conway service is running"}
