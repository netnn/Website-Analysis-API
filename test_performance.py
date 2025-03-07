import csv
import subprocess
import json
from datetime import datetime


class TestWebsitePerformance:
    # The URL to be tested.
    url = "https://www.cbssports.com/betting"

    # Get the current date and time
    timestamp = datetime.now ().strftime ("%Y-%m-%d")

    def test_lighthouse(self):
        """
        This function uses Google Lighthouse to analyze the website's performance, accessibility, SEO, and best practices.
        The Lighthouse report is generated in JSON format and then processed to extract scores.
        Finally, the scores are saved into a CSV file.

        Approach:
        1. Run Lighthouse via CLI using subprocess with shell=True (for Windows compatibility).
        2. Load the generated JSON report.
        3. Extract key scores from the 'categories' section.
        4. Save the results as a CSV file, which can be used for historical tracking.

        How it helps monitor websites:
        - By running this script periodically (through a CI/CD pipeline or a scheduled task),
          you can track changes in website performance and other key metrics over time.
        - I suggest storing the records in a database (DB) and comparing current metrics with median values.
        - The CSV reports allow you to analyze trends, detect regressions, and plan improvements.
        """

        # This command runs Lighthouse in quiet mode with headless Chrome.
        command = (
            f"lighthouse {self.url} "
            "--quiet "
            "--chrome-flags=--headless "
            "--output=json "
            "--output-path=./lighthouse-report.json"
        )

        # Run the Lighthouse command via subprocess (shell=True for Windows compatibility)
        subprocess.run (command, check=True, shell=True)

        # Read the Lighthouse JSON report
        with open ("lighthouse-report.json", "r", encoding="utf-8") as f:
            data = json.load (f)

        # Extract scores from the report
        results = {
            "performance": data['categories']['performance']['score'],
            "accessibility": data['categories']['accessibility']['score'],
            "best_practices": data['categories']['best-practices']['score'],
            "seo": data['categories']['seo']['score']
        }

        # Write the results to a CSV file
        with open (f"lighthouse-scores_{self.timestamp}_report.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["category", "score"]
            writer = csv.DictWriter (csvfile, fieldnames=fieldnames)
            writer.writeheader ()
            for category, score in results.items ():
                writer.writerow ({"category": category, "score": score})

    def test_resource_validation(self, page):
        """
        This function uses Playwright to navigate to the website and monitors network requests.
        It collects any requests that return a status code other than 200.
        The broken requests are then saved into a CSV file for further analysis.

        Approach:
        1. Listen for 'requestfinished' events and capture each request's URL and response status.
        2. After the page fully loads (wait_until "networkidle"), filter out requests with non-200 status codes.
        3. Save the broken requests into a CSV file.

        How it helps monitor websites:
        - This script can be run periodically to verify that all resources (images, scripts, styles)
          are loading correctly on the site.
        """
        broken_requests = []

        # Function to handle each finished request and store if the status is not 200
        def on_request_finished(request):
            response = request.response ()
            if response and response.status != 200:
                broken_requests.append ({
                    "url": request.url,
                    "status": response.status
                })

        # Register the handler for 'requestfinished' events
        page.on ("requestfinished", on_request_finished)

        # Navigate to the website and wait until the network is idle (all requests finished)
        page.goto (self.url, wait_until="networkidle")

        # Write broken requests to a CSV file
        with open (f"broken_requests_{self.timestamp}_report.csv", "w", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["url", "status"]
            writer = csv.DictWriter (csv_file, fieldnames=fieldnames)
            writer.writeheader ()
            for request_info in broken_requests:
                writer.writerow (request_info)
