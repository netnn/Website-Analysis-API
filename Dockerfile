# Use a slim Python image
FROM python:3.9-slim

# Install system dependencies required for Playwright and Lighthouse
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    curl \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0

# Install Node.js (required for Lighthouse)
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs

# Install Lighthouse globally via npm
RUN npm install -g lighthouse

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Install Playwright browsers
RUN python -m playwright install

# Default command: run pytest with the target URL parameter (ניתן לשנות לפי הצורך)
CMD ["pytest", "--target-url", "https://www.cbssports.com/betting"]
