import requests
import re
import numpy as np
import folium
from folium import plugins
from bs4 import BeautifulSoup
import json

def get_country_urls(country_codes, headers):
    urls = []

    for code in country_codes:
        url = f"http://www.insecam.org/en/bycountry/{code}/"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            urls.append(url)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")

    return urls

def scrape_image_urls(base_url, headers):
    total_urls = []

    try:
        page = requests.get(base_url, headers=headers)
        page.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
        num_pages = soup.find('ul', class_='pagination')

        paragraphs = []
        for x in num_pages:
            paragraphs.append(str(x))

        list_as_str = ''.join(map(str, paragraphs))
        page_count = re.search(r'\d+', list_as_str).group()

        for count in range(0, int(page_count)):
            new_url = f"{base_url}?page={count}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            }

            content = requests.get(new_url, headers=headers).content
            soup = BeautifulSoup(content, 'lxml')  # choose lxml parser
            image_tags = soup.findAll('img')

            for image_tag in image_tags:
                u = image_tag.get('src')
                total_urls.append(u)

    except requests.exceptions.RequestException as e:
        print(f"Error scraping image URLs for {base_url}: {e}")

    return total_urls

def filter_yandex_urls(urls):
    prefixes = ('https://mc.yandex.ru/watch/41237994')
    filtered_urls = [url for url in urls if not url.startswith(prefixes)]
    return filtered_urls

def get_geo_coordinates(ip_addresses):
    latitudes = []
    longitudes = []

    for ip_address in ip_addresses:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            }

            response = requests.get(f'http://freegeoip.net/json/{ip_address}', headers=headers)
            response.raise_for_status()  # Check for HTTP errors

            parsed_json = json.loads(response.text)
            latitudes.append(parsed_json['latitude'])
            longitudes.append(parsed_json['longitude'])

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error getting coordinates for {ip_address}: {e}")

    return latitudes, longitudes

def create_folium_map(locations, popup_texts):
    map = folium.Map(zoom_start=12)
    plugins.Terminator().add_to(map)
    
    # Use MarkerCluster from plugins submodule
    marker_cluster = plugins.MarkerCluster().add_to(map)

    for point, popup_text in zip(locations, popup_texts):
        folium.Marker(point, popup=popup_text).add_to(marker_cluster)

    map.save("C:/Users/Human/Desktop/unsecured_cams_map.html")

# Main script
country_codes = ['IN']
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

# Step 1: Get country URLs
country_urls = get_country_urls(country_codes, headers)
print(country_urls)

# Step 2: Scrape image URLs
all_image_urls = []
for country_url in country_urls:
    image_urls = scrape_image_urls(country_url, headers)
    all_image_urls.extend(image_urls)

# Step 3: Filter Yandex URLs
filtered_urls = filter_yandex_urls(all_image_urls)

# Step 4: Get unique IP addresses
unique_ip_addresses = np.unique([re.findall(r'[0-9]+(?:\.[0-9]+){3}', url)[0] if re.findall(r'[0-9]+(?:\.[0-9]+){3}', url) else '' for url in filtered_urls])

# Step 5: Get geo-coordinates
latitudes, longitudes = get_geo_coordinates(unique_ip_addresses)

# Step 6: Create Folium map
formatted_latitudes = ['%.2f' % elem for elem in latitudes]
formatted_longitudes = ['%.2f' % elem for elem in longitudes]
formatted_latitudes = [float(i) for i in formatted_latitudes]
formatted_longitudes = [float(i) for i in formatted_longitudes]

coordinates = lambda lat, lon: [list(coord) for coord in zip(lat, lon)]
locations = coordinates(formatted_latitudes, formatted_longitudes)

create_folium_map(locations, filtered_urls)
