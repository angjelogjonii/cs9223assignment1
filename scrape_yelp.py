import requests
import json
import time
import boto3

YELP_API_KEY = "m5pctBWd-kGwpVDrlrWpkU_Ud_kLbV0WSelUlOiuQzSBCX9F2hiSPnN8ZDD7hghu0Wynae054apjvJluQ5GDiOBNeXLPZkm5iEoOKg4X2mxVTay53xl1LWYl_a--Z3Yx"
HEADERS = {"Authorization": f"Bearer {YELP_API_KEY}"}
YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"

# AWS DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("yelp-restaurants")

# Search settings
LOCATION = "Manhattan, NY"
CUISINES = ["Italian", "Chinese", "Mexican", "Japanese", "Indian"]
LIMIT = 50
TOTAL_RESTAURANTS = 1000

def fetch_restaurants(cuisine):
    restaurants = []
    for offset in range(0, TOTAL_RESTAURANTS, LIMIT):
        params = {
            "location": LOCATION,
            "term": f"{cuisine} restaurants",
            "limit": LIMIT,
            "offset": offset
        }
        response = requests.get(YELP_SEARCH_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            restaurants.extend(data.get("businesses", []))
        else:
            print(f"Error fetching {cuisine}: {response.text}")
        time.sleep(1)  # Prevent hitting API rate limits
    return restaurants

# Function to insert data into DynamoDB
def store_in_dynamodb(restaurants):
    for r in restaurants:
        try:
            table.put_item(
                Item={
                    "business_id": r["id"],
                    "name": r["name"],
                    "address": " ".join(r["location"]["display_address"]),
                    "coordinates": r["coordinates"],
                    "review_count": r.get("review_count", 0),
                    "rating": r.get("rating", 0),
                    "zip_code": r["location"]["zip_code"],
                    "cuisine": r["categories"][0]["title"],
                    "insertedAtTimestamp": int(time.time())
                }
            )
            print(f"Inserted {r['name']} into DynamoDB.")
        except Exception as e:
            print(f"Error inserting {r['name']}: {e}")

# Scrape data and store in DynamoDB
all_restaurants = []
for cuisine in CUISINES:
    print(f"Fetching {cuisine} restaurants...")
    cuisine_data = fetch_restaurants(cuisine)
    all_restaurants.extend(cuisine_data)
    store_in_dynamodb(cuisine_data)

print(f"✅ Successfully stored {len(all_restaurants)} restaurants in DynamoDB!")
