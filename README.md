# Website-Analysis-API
"Automation scripts for website performance analysis (Lighthouse and Playwright) and API data validation (pytest)."
Below is a sample `README.md` file for your repository:

---

# Website Analysis

**Automation scripts for website performance testing and resource validation (using Lighthouse and Playwright), along with API data retrieval and validation using pytest.**

## Overview

This repository contains automation scripts to help monitor and validate both website performance and API data integrity. The project is divided into two main sections:

1. **Website Analysis and Validation**
   - **Performance Testing:**  
     Uses [Google Lighthouse](https://developers.google.com/web/tools/lighthouse) to analyze key performance metrics, accessibility, SEO, and best practices. The resulting report is saved in JSON format and key scores are extracted into a CSV file.
   - **Resource Validation:**  
     Utilizes [Playwright](https://playwright.dev) to navigate the website and verify that all resources (CSS, JS, images) load correctly. Any broken requests (non-200 status codes) are logged into a CSV file for further analysis.

2. **API Data Retrieval and Validation**
   - **Data Fetching:**  
     Retrieves a list of posts from [JSONPlaceholder](https://jsonplaceholder.typicode.com/posts).
   - **Data Validation:**  
     Uses [pytest](https://docs.pytest.org) to validate that each post has:
     - A numeric `userId`.
     - A non-empty `title`.
     - A non-empty `body`.
     
     Each post is treated as an individual test case, and detailed error messages are provided for any failures.

## Repository Structure

- **test_posts_api.py**  
  Script for fetching and validating API data using pytest.

- **test_performance.py**  
  Script that performs website performance analysis using Lighthouse and resource validation using Playwright.

- **conftest.py**  
  Pytest configuration file setting up fixtures for Playwright browser context and pages.

## Prerequisites

### System Requirements
- **Python 3.x**
- **Node.js and npm** (for installing Lighthouse)
- **Playwright** (including installation of browsers)

### Python Dependencies
- `pytest`
- `requests`
- `playwright`

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/netnn/Website-Analysis-API.git
cd Website-Analysis-API

```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
venv\Scripts\activate      # For Windows
source venv/bin/activate   # For Linux/Mac
```

### 3. Install Python Dependencies

If you have a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages manually:

```bash
pip install pytest requests playwright
```

### 4. Install Playwright Browsers

```bash
playwright install
```

### 5. Install Google Lighthouse (Windows)

```bash
npm install -g lighthouse
```

## Running the Scripts

### Running API Tests

To validate API data using pytest, run:

```bash
pytest -v test_posts_api.py
```

This command fetches posts from JSONPlaceholder and validates each post according to the defined criteria.

### Running Performance and Resource Validation Tests

To analyze website performance, run:

```bash
pytest -k test_lighthouse -v test_performance.py
```
To validate resources, run:

```bash
pytest -k test_resource_validation -v test_performance.py
```

This script will:
- Execute Google Lighthouse on the specified website, generate a JSON report, extract key scores, and export them to a CSV file.
- Use Playwright to monitor the website’s network requests, logging any broken resource requests (non-200 status codes) to a CSV file.

## How It Works

### Website Analysis and Resource Validation
- **Lighthouse:**  
  The script runs Lighthouse using Python’s `subprocess` module to generate a JSON report. The report is parsed to extract scores for performance, accessibility, SEO, and best practices. These scores are then saved in a CSV file for historical tracking and analysis.
  
- **Playwright:**  
  The script listens for network events as the page loads. It captures all requests, and any requests that return a status code other than 200 are logged into a CSV file for further analysis.

### API Data Retrieval and Validation
- The API test script retrieves posts from JSONPlaceholder.
- Each post is validated using pytest to ensure that:
  - `userId` is a number.
  - `title` is not empty.
  - `body` is not empty.
- Detailed error messages are printed for any post that does not meet the criteria.
