import requests
import json
import os
from apscheduler.schedulers.blocking import BlockingScheduler

# Set up the scheduler
scheduler = BlockingScheduler()

# Retrieve New Relic API key from environment variable
new_relic_insert_key = os.getenv('NEW_RELIC_API_KEY')
if not new_relic_insert_key:
    raise ValueError("No New Relic API key found. Set the NEW_RELIC_API_KEY environment variable.")

# Your Google PageSpeed API Key
google_api_key = os.getenv('GOOGLE_API_KEY')
if not google_api_key:
    raise ValueError("No Google API key found. Set the GOOGLE_API_KEY environment variable.")

# Your New Relic Account ID
new_relic_account_id = '4275397'

# Your Google PageSpeed API Key
google_api_key = 'YOUR_GOOGLE_API_KEY'

# The URL you want to check
url_to_check = 'https://www.example.com'

def fetch_lighthouse_data():
    # Call the Google PageSpeed Insights API
    api_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url_to_check}&key={google_api_key}'
    response = requests.get(api_url)
    data = response.json()

    # Extract the necessary metrics from the response
    metrics = {
        'firstContentfulPaint': data['lighthouseResult']['audits']['first-contentful-paint']['numericValue'],
        'largestContentfulPaint': data['lighthouseResult']['audits']['largest-contentful-paint']['numericValue'],
        # Add other metrics as necessary
    }

    # Format data for New Relic
    new_relic_data = {
        'eventType': 'LighthouseMetrics',
        'url': url_to_check,
        **metrics
    }

    # Send data to New Relic
    headers = {
        'Api-Key': new_relic_insert_key,
        'Content-Type': 'application/json'
    }
    nr_url =f'https://insights-collector.eu01.nr-data.net/v1/accounts/{new_relic_account_id}/events'
    
    requests.post(nr_url, headers=headers, data=json.dumps([new_relic_data]))

# Schedule the function to run every hour (for example)
scheduler.add_job(fetch_lighthouse_data, 'interval', hours=1)

# Start the scheduler
scheduler.start()
