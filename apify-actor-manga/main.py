from apify_client import ApifyClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the ApifyClient with API token from environment
client = ApifyClient(os.getenv('APIFY_API_TOKEN'))

# Prepare the Actor input
run_input = {
    "url": "https://www.viz.com/shonenjump/chainsaw-man-chapter-216/chapter/47669?action=read",
    "startingChapter": 216,
    "endingChapter": 216,
    "language": "en",
    "format": "cbz",
}

# Run the Actor and wait for it to finish
run = client.actor("panjan/comick-io").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)

# 📚 Want to learn more 📖? Go to → https://docs.apify.com/api/client/python/docs/quick-start
