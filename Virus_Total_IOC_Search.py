import requests
import json
#update API_KEY here
API_KEY = 'paste API key here'

def check_ioc(ioc):
    """
    Queries the Virustotal API for information on the given IOC.
    """
    url = 'https://www.virustotal.com/api/v3/ip_addresses/{}' if '.' in ioc else 'https://www.virustotal.com/api/v3/domains/{}'
    headers = {'x-apikey': API_KEY}
    response = requests.get(url.format(ioc), headers=headers)

    if response.status_code == 200:
        result = json.loads(response.text)
        attributes = result['data']['attributes']
        print(f"IOC: {ioc}")
        print(f"Last analysis date: {attributes['last_analysis_date']}")
        print(f"Number of positive detections: {attributes['last_analysis_stats']['malicious']}")
        print(f"Number of engines that detected the IOC: {attributes['last_analysis_stats']['malicious'] + attributes['last_analysis_stats']['suspicious']}")
        print(f"Additional information: {attributes['whois']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Example usage
check_ioc('8.8.8.8')