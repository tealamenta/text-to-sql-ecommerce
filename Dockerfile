FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY data/ data/
COPY run.py .
COPY pyproject.toml .

# Install package
RUN pip install -e .

# Expose port
EXPOSE 8000

# Run API
CMD ["python", "run.py", "api"]
