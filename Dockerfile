FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose the port
EXPOSE 5000

# Set environment variables
ENV PORT=5000
ENV FILE_DIR=files

# Run the application
CMD ["python", "app.py"]