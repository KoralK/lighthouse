import json
import requests
import logging

def parse_lighthouse_report(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

lighthouse_data = parse_lighthouse_report('report.json')

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

new_relic_data = extract_metrics(lighthouse_data)

def print_data_for_verification(data):
    print("Data to be sent to New Relic:")
    print(json.dumps(data, indent=4))

print_data_for_verification(new_relic_data)

def send_data_to_new_relic(data):
    logging.basicConfig(level=logging.DEBUG)
    headers = {
        "Api-Key": "eu01xx527745a1e9849a14fa3a5df19bb731NRAL",
        "Content-Type": "application/json"
    }
    url = "https://insights-collector.newrelic.com/v1/accounts/YOUR_ACCOUNT_ID/events"  # Replace YOUR_ACCOUNT_ID with your actual account ID

    response = requests.post(url, headers=headers, json=[data])

    try:
        response.raise_for_status()
        print("Sent metrics successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

    return response

send_response = send_data_to_new_relic(new_relic_data)
