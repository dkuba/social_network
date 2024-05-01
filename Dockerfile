# Base image
FROM python:3.11-slim-buster

# Create a user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /usr/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app .

# Set ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /usr/app

# Run the application as non-root user
USER appuser

ENV PYTHONPATH "${PYTHONPATH}:/usr"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]