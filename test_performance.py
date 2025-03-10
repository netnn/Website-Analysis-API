import csv
import subprocess
import json
import pytest
from datetime import datetime

class TestWebsitePerformance:
    # Get the current date and time for naming output files
    timestamp = datetime.now().strftime("%Y-%m-%d")

    def test_lighthouse(self, target_url):
        """
        Uses Google Lighthouse to analyze website performance, accessibility, SEO, and best practices.
        The resulting report is processed and key scores are saved into a CSV file.
        """
        command = (
            f"lighthouse {target_url} "
            "--quiet "
            "--chrome-flags=\"--headless --no-sandbox\" "
            "--output=json "
            "--output-path=./lighthouse-report.json"
        )
        try:
            # Capture stdout and stderr for detailed error info
            result = subprocess.run (command, check=True, shell=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail (f"Lighthouse command failed: {e}\nStdout: {e.stdout}\nStderr: {e.stderr}")

        try:
            with open ("lighthouse-report.json", "r", encoding="utf-8") as f:
                data = json.load (f)
        except Exception as e:
            pytest.fail (f"Failed to read Lighthouse report: {e}")

        try:
            results = {
                "performance": data['categories']['performance']['score'],
                "accessibility": data['categories']['accessibility']['score'],
                "best_practices": data['categories']['best-practices']['score'],
                "seo": data['categories']['seo']['score']
            }
            with open (f"lighthouse-scores_{self.timestamp}_report.csv", "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["category", "score"]
                writer = csv.DictWriter (csvfile, fieldnames=fieldnames)
                writer.writeheader ()
                for category, score in results.items ():
                    writer.writerow ({"category": category, "score": score})
        except Exception as e:
            pytest.fail (f"Failed to process Lighthouse report data or write CSV: {e}")

    def test_resource_validation(self, page, target_url):
        """
        Uses Playwright to navigate to the website and monitors network requests.
        Any request that returns a status code other than 200 is logged and saved into a CSV file.
        """
        broken_requests = []

        def on_request_finished(request):
            try:
                response = request.response()
                if response and response.status != 200:
                    broken_requests.append({
                        "url": request.url,
                        "status": response.status
                    })
            except Exception as e:
                print(f"Error processing request {request.url}: {e}")

        page.on("requestfinished", on_request_finished)

        try:
            page.goto(target_url, wait_until="networkidle")
        except Exception as e:
            pytest.fail(f"Page navigation failed for {target_url}: {e}")

        try:
            with open(f"broken_requests_{self.timestamp}_report.csv", "w", newline="", encoding="utf-8") as csv_file:
                fieldnames = ["url", "status"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for request_info in broken_requests:
                    writer.writerow(request_info)
        except Exception as e:
            pytest.fail(f"Failed to write broken requests CSV report: {e}")
