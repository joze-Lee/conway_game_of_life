# Use official Python base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app


# Install GPT tool dependencies if separate

RUN pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "conway_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
