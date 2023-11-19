import pandas as pd
import requests
import zipfile
from io import BytesIO

# Download the zip file from the URL
url = 'http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip'
response = requests.get(url)
zipfile_data = BytesIO(response.content)

# Extract the CSV file from the zip file
with zipfile.ZipFile(zipfile_data) as zip_file:
    csv_filename = zip_file.namelist()[0]
    csv_data = zip_file.read(csv_filename)

# Convert the CSV data to a pandas DataFrame
df = pd.read_csv(BytesIO(csv_data), header=None, names=['rank', 'website'])
