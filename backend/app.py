from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import torch
from transformers import pipeline
from flask import Flask, jsonify, request
from flask_cors import CORS

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for servers
chrome_options.add_argument("--disable-gpu")  # Disable GPU for server environments
chrome_options.add_argument("--no-sandbox")  # Prevent sandbox issues
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/values", methods=["POST", "GET"])
def value():
    driver = None  # Initialize driver as None at the start of each request
    try:
        # Handle GET and POST requests
        if request.method == "GET":
            query = request.args.get("query", default="masters")  # Default to "masters" if not provided
        elif request.method == "POST":
            data = request.get_json()
            query = data.get("query", "masters")  # Default to "masters" if not provided

        # Initialize WebDriver within the request
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Prepare search URL
        search_url = f"https://www.google.com/search?q={query}"
        driver.get(search_url)

        # Give it some time to load
        time.sleep(3)

        # Extracting the titles and descriptions from the search results
        search_results = driver.find_elements(By.CSS_SELECTOR, ".tF2Cxc")

        # List to store the extracted data temporarily
        extracted_data = []

        for result in search_results:
            try:
                # Get the title and URL from the search result
                title = result.find_element(By.CSS_SELECTOR, ".DKV0Md").text
                url = result.find_element(By.CSS_SELECTOR, ".yuRUbf a").get_attribute("href")

                # Temporarily store the extracted data
                data = {"title": title, "url": url}
                extracted_data.append(data)

                # Navigate to the URL and extract paragraphs
                driver.get(url)
                time.sleep(3)
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                paragraph_texts = [p.text for p in paragraphs if p.text.strip()]
                data["paragraphs"] = paragraph_texts

            except Exception as e:
                print(f"Error processing result: {e}")

        # Combine extracted paragraphs for summarization
        extracted_text = "\n".join(
            [entry["paragraphs"][0] for entry in extracted_data if "paragraphs" in entry and entry["paragraphs"]]
        )

        # Initialize Hugging Face pipelines
        summarization_pipeline = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1
        )
        ner_pipeline = pipeline(
            "ner",
            grouped_entities=True,
            device=0 if torch.cuda.is_available() else -1
        )

        # Generate summary
        outputs = summarization_pipeline(extracted_text, max_length=150)
        response = outputs[0]["summary_text"]

        # Perform Named Entity Recognition
        entities = ner_pipeline(response)
        entity_data = [{"word": entity["word"], "type": entity["entity_group"]} for entity in entities]

        # Return the response
        return jsonify({"status": "200", "summary": response, "entities": entity_data})

    except Exception as e:
        return jsonify({"status": "500", "error": str(e)})

    finally:
        # Ensure the driver is closed after each request
        if driver:
            driver.quit()

if __name__ == "__main__":
    app.run(debug=True)
