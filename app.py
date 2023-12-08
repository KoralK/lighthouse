#https://docs.newrelic.com/docs/data-apis/ingest-apis/event-api/introduction-event-api/
import json
import requests
import logging

def parse_lighthouse_report(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

lighthouse_data = parse_lighthouse_report('report.json')

def extract_metrics(lighthouse_data):
    performance_score = lighthouse_data['categories']['performance']['score'] * 100
    return {
        "eventType": "LighthouseAudit",
        "performanceScore": performance_score
    }

new_relic_data = extract_metrics(lighthouse_data)

def print_data_for_verification(data):
    print("Data to be sent to New Relic:")
    print(json.dumps(data, indent=4))

print_data_for_verification(new_relic_data)

def send_data_to_new_relic(data):
    logging.basicConfig(level=logging.DEBUG)
    headers = {
        "Api-Key": "d9e702fe3d0e770f55a57e9ad279d8d0FFFFNRAL",  # Replace with your actual API key
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
