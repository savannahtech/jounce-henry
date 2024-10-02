# Use the official Python image as the base image for the builder stage
FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies and clean up afterwards to reduce image size
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for dependencies
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Final stage - smaller image for running the app
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Create the app user
RUN addgroup --system app && adduser --system --ingroup app app

# Install system dependencies and clean up after installation
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the wheels from the builder stage and install dependencies
COPY --from=builder /wheels /wheels
RUN pip install --upgrade pip && pip install --no-cache /wheels/*

# Copy the application code
COPY . .

# Set proper permissions for the app directory
RUN chown -R app:app /app

# Switch to non-root user for security
USER app

# Expose port 8000 and run Uvicorn server
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
