# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements into the image
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers in the image
RUN playwright install --with-deps

# Copy the entire source code into the image
COPY . .

# Set the module path
ENV PYTHONPATH=/app

# Default command (optional)
CMD ["python","-m","pytest", "-s", "-v", "tests/"]