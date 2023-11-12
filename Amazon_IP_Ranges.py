# pip install requests
# pip install pandas
import requests
import pandas as pd

# Set the URL for the AWS IP Ranges JSON file
url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()

    # Extract relevant information for DataFrame
    prefixes = data.get("prefixes", [])
    rows = []

    for prefix in prefixes:
        ip_prefix = prefix.get("ip_prefix")
        region = prefix.get("region")
        service = prefix.get("service")
        network_border_group = prefix.get("network_border_group")

        rows.append({
            "ip_prefix": ip_prefix,
            "region": region,
            "service": service,
            "network_border_group": network_border_group
        })

    # Create a DataFrame from the extracted information
    df = pd.DataFrame(rows)

    # Display the DataFrame
    print(df)

else:
    # Print the error message if the request failed
    print("Failed to retrieve AWS IP ranges:", response.text)
