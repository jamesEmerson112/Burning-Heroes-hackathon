# Apify Actor - Manga Downloader

Python script to download manga chapters from Comick.io using the Apify platform.

## Setup Instructions

### 1. Clone or Navigate to Project

```bash
cd apify-actor-manga
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Apify API token:
   ```
   APIFY_API_TOKEN=your_actual_api_token_here
   ```

3. Get your API token from: https://console.apify.com/account/integrations

## Usage

Run the script with the virtual environment activated:

```bash
python main.py
```

The script will:
- Download chapters 1-5 of "Sousou no Frieren" from Comick.io
- Save them in CBZ format
- Display the dataset URL where results are stored

## Configuration

Edit the `run_input` dictionary in `main.py` to customize:
- `url`: The manga URL on Comick.io
- `startingChapter`: First chapter to download
- `endingChapter`: Last chapter to download
- `language`: Language code (e.g., "en" for English)
- `format`: Output format ("cbz" or "pdf")

## Dependencies

- `apify-client`: Apify API client for Python
- `python-dotenv`: Environment variable management

## Documentation

For more information about the Apify Actor used:
- Actor: https://apify.com/panjan/comick-io
- Apify Python Client: https://docs.apify.com/api/client/python/docs/quick-start
