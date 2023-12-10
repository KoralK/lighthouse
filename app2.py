import json
import requests
import logging
import os
import pytest

# Ensure the NEW_RELIC_API_KEY environment variable is set
api_key = os.getenv('NEW_RELIC_API_KEY')
if not api_key:
    raise ValueError("No API key found. Set the NEW_RELIC_API_KEY environment variable.")

def parse_lighthouse_report(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_metrics(lighthouse_data):
    # Extracting key metrics
    fcp = lighthouse_data['audits']['first-contentful-paint']['numericValue']
    lcp = lighthouse_data['audits']['largest-contentful-paint']['numericValue']
    speed_index = lighthouse_data['audits']['speed-index']['numericValue']
    
    return {
        "eventType": "LighthouseAudit",
        "firstContentfulPaint": fcp,
        "largestContentfulPaint": lcp,
        "speedIndex": speed_index
    }

def print_data_for_verification(data):
    print("Data to be sent to New Relic:")
    print(json.dumps(data, indent=4))

def send_data_to_new_relic(data):
    logging.basicConfig(level=logging.DEBUG)
    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    # Replace YOUR_ACCOUNT_ID with your actual account ID
    url = "https://insights-collector.newrelic.com/v1/accounts/4275397/events"

    response = requests.post(url, headers=headers, json=[data])

    try:
        response.raise_for_status()
        print("Sent metrics successfully!")
    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    return response

# Running the script
if __name__ == "__main__":
    lighthouse_data = parse_lighthouse_report('report.json')
    new_relic_data = extract_metrics(lighthouse_data)
    print_data_for_verification(new_relic_data)
    send_response = send_data_to_new_relic(new_relic_data)