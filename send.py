from newrelic_telemetry_sdk import MetricClient

def send_data_to_new_relic(data):
    # Make sure to keep your API keys secret.
    # Do not hardcode them in your code, especially if it's shared publicly.
    # Instead, use environment variables or other secure means to store them.
    insert_key = "d9e702fe3d0e770f55a57e9ad279d8d0FFFFNRAL"  # Replace with your actual Ingest - License key
    client = MetricClient(insert_key)
    response = client.send(data)
    return response

# Make sure 'new_relic_data' is the correctly formatted data you wish to send
send_response = send_data_to_new_relic(new_relic_data)
print("Response from New Relic:", send_response)
