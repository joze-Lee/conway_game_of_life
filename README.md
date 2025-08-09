# Monument AI – Conway’s Game of Life Challenge

## Overview
This project is a solution to **Monument AI’s technical challenge**.  
It implements a RESTful web service for a variation of Conway’s Game of Life, seeded from the ASCII binary representation of a given English word.

The API returns:
- **Generations** → Number of generations until stability is reached  
- **Score** → Total number of cells spawned during execution  

A **Generative AI tool (Python)** wraps the API so `gpt-4o-mini` can call it directly and answer natural language prompts.

---

## Tech Stack
- **Backend:** Python + FastAPI  
- **Frontend:** HTML / CSS / JavaScript (Glassmorphism UI)  
- **AI Integration:** GPT-4o-mini  
- **Deployment:** Docker + AWS EC2 + Nginx  

---

## Features
- Converts an English word into an ASCII binary seed pattern  
- Initializes a **60×40 grid** and seeds the pattern at the center  
- Runs Conway’s Game of Life until stability:
  - Extinction  
  - Persistent state  
  - Periodic pattern (< 10 generations)  
  - Maximum 1000 generations  
- Returns:
  - `generations` → Number until stability  
  - `score` → Total number of cells spawned  
- Supports two primary prompt formats:
  1. `"How many generations will the word 'monument' return from the Conway tool?"`
  2. `"Generate 3 random words and tell me the highest Conway score."`  
- Responsive, glassmorphism-inspired frontend  
- Dockerized deployment for portability  
- Nginx reverse proxy for serving frontend & backend seamlessly  

---

## API Endpoints
## 1. Conway Simulation: Word-based Prompt  
**POST** `/prompt`  
**Request Body:**  
```json
{
  "prompt": "How many generations will the word 'monument' return from the Conway tool?"
}
```

## 2. Conway Simulation: Random Words Prompt  
**POST** `/prompt`  
**Request Body:**  
```json
{
  "prompt": "Generate 3 random words and tell me the highest Conway score."
}
```

---

## System Architecture  
```
[Frontend UI] → [Nginx Reverse Proxy] → [FastAPI Backend] → [Conway Logic Engine]  
                                           ↳ [Generative AI Wrapper → GPT-4o-mini]
```

---

## Deployment  
This project is Dockerized for portability and deployed on **AWS EC2**:

- **Nginx** serves the frontend and proxies API requests to the backend  
- **Docker** ensures a consistent environment and easy redeployment  
- **EC2 Security Groups** restrict public access to only necessary ports  

---

## Repository Structure  
```
.
├── conway_api/       # FastAPI backend with Conway's Game of Life logic  
├── gtp_tools/        # Wrapper for the Generative AI prompt  
├── frontend/         # HTML, CSS, and JavaScript frontend  
├── docker/           # Docker configuration files  
├── README.md         # Project documentation  
└── requirements.txt  # Python dependencies  
```

---

## License  
This project was developed as part of **Monument AI’s technical challenge** and is intended for demonstration purposes.
