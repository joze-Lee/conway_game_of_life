import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conway_api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "message": "Conway service is running"}

def test_simulate_valid_word():
    response = client.get("/simulate", params={"word": "monument"})
    assert response.status_code == 200
    data = response.json()
    assert "generations" in data
    assert "score" in data
    assert "state" in data

def test_simulate_non_ascii_word():
    response = client.get("/simulate", params={"word": "mønument"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Word must contain only ASCII characters"

def test_simulate_empty_word():
    response = client.get("/simulate", params={"word": ""})
    assert response.status_code == 422  # Validation error for empty word

def test_prompt_valid_generations():
    prompt = "How many generations will the word ‘monument’ return from the Conway tool?"
    response = client.post("/prompt", params={"prompt": prompt})
    assert response.status_code == 200
    data = response.json()
    assert "monument" in data["response"]
    assert "generations" in data["response"]
    assert "score" in data["response"]

def test_prompt_valid_random_words():
    prompt = "Generate 3 random words and tell me the highest Conway score."
    response = client.post("/prompt", params={"prompt": prompt})
    assert response.status_code == 200
    data = response.json()
    assert "Generated words:" in data["response"]
    assert "Highest Conway score" in data["response"]

def test_prompt_unrecognized():
    prompt = "Tell me the weather today"
    response = client.post("/prompt", params={"prompt": prompt})
    assert response.status_code == 200
    assert response.json()["response"] == "Sorry, I couldn't understand the prompt."

def test_prompt_empty():
    response = client.post("/prompt", params={"prompt": ""})
    assert response.status_code == 422  # Validation error for empty prompt
