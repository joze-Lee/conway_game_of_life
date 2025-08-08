# conway_api/main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from conway_api.conway import run_until_stable
from gpt_tool.gpt_tool import ConwayGPTTool 


app = FastAPI(
    title="Monument AI Conway Service",
    description="Simulates Conway’s Game of Life seeded with ASCII binary of a word",
    version="1.0.0"
)

conway_tool = ConwayGPTTool()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationResult(BaseModel):
    generations: int
    score: int
    state: str

class PromptResponse(BaseModel):
    response: str

@app.get("/simulate", response_model=SimulationResult)
def simulate(word: str = Query(..., min_length=1, description="Seed word for Conway grid")):
    """
    Simulates Conway's Game of Life using ASCII binary of the word as seed.
    Returns generation count, score, and final state.
    """
    if not word.isascii():
        raise HTTPException(status_code=400, detail="Word must contain only ASCII characters")
    try:
        result = run_until_stable(seed_word=word)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")
    return SimulationResult(**result)


@app.get("/")
def health_check():
    return {"status": "OK", "message": "Conway service is running"}

@app.post("/prompt", response_model=PromptResponse)
def prompt_endpoint(prompt: str = Query(..., min_length=1, description="User prompt for Conway GPT Tool")):
    """
    Accepts a user prompt, processes it via ConwayGPTTool, and returns the response string.
    Supports prompts like:
    - "How many generations will the word 'monument' return from the Conway tool?"
    - "Generate 3 random words and tell me the highest Conway score."
    """
    try:
        response_text = conway_tool.handle_prompt(prompt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing prompt: {str(e)}")

    return PromptResponse(response=response_text)