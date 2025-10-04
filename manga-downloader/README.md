# MangaDex API Demo - Manga Downloader

A simple JavaScript client to interact with the MangaDex API. This demo searches for "Chainsaw Man" and displays manga information, chapters, and detailed chapter data.

## Features

- 🔍 Search manga by title
- 📚 Get manga chapters with pagination
- 📄 Get detailed chapter information
- 🖼️ Support for retrieving chapter image URLs
- ⚡ Built-in rate limiting to respect API limits
- 🎨 Formatted console output with emojis

## Prerequisites

- Node.js 16.x or higher
- npm or yarn

## Installation

1. Navigate to the project directory:
```bash
cd manga-downloader
```

2. Install dependencies:
```bash
npm install
```

## Usage

### Search by Manga Name

```bash
# Search for manga by name
npm start "Chainsaw Man"

# Search with specific chapter
npm start "Chainsaw Man" 216
```

### Search by Manga ID

```bash
# Search for manga by ID (UUID)
npm start "a77742b1-befd-49a4-bff5-1ad4e6b0ef7b"

# Search by ID with specific chapter
npm start "a77742b1-befd-49a4-bff5-1ad4e6b0ef7b" 216
```

The program automatically detects whether you're searching by name or ID based on the UUID format.

### What happens when you run it:

**Search by Name:**
1. Searches for manga matching the title
2. Displays up to 5 search results with manga details
3. Selects the first (most relevant) result
4. Fetches chapters and shows details

**Search by ID:**
1. Directly fetches the manga by its UUID
2. Displays the manga details
3. Fetches chapters and shows details

### Expected Output

```
╔════════════════════════════════════════════════════════════════════════════╗
║              MangaDex API Demo - Chainsaw Man                              ║
╚════════════════════════════════════════════════════════════════════════════╝

📚 Searching for "Chainsaw Man"...

✅ Found X manga matching "Chainsaw Man"

SEARCH RESULTS
[Details of found manga...]

CHAPTER LIST
[List of chapters with IDs, pages, etc...]

DETAILED CHAPTER INFORMATION
[Detailed info for first 3 chapters...]
```

## Project Structure

```
manga-downloader/
├── package.json          # Project configuration and dependencies
├── index.js              # Main application entry point
├── lib/
│   ├── mangadex.js      # MangaDex API client
│   └── utils.js         # Utility functions for formatting and display
└── README.md            # This file
```

## API Endpoints Used

### 1. Search Manga
```
GET https://api.mangadex.org/manga?title={query}
```
Search for manga by title with optional filters.

### 2. Get Manga Chapters
```
GET https://api.mangadex.org/manga/{mangaId}/feed
```
Retrieve chapters for a specific manga with language filtering and pagination.

### 3. Get Chapter Details
```
GET https://api.mangadex.org/chapter/{chapterId}
```
Get detailed information about a specific chapter.

### 4. Get Chapter Images (Bonus)
```
GET https://api.mangadex.org/at-home/server/{chapterId}
```
Retrieve image URLs for downloading chapter pages.

## MangaDex API Client Usage

### Import the Client

```javascript
import MangaDexClient from './lib/mangadex.js';

const client = new MangaDexClient();
```

### Search for Manga

```javascript
const results = await client.searchManga('Chainsaw Man', {
  limit: 10  // Optional
});
```

### Get Manga Chapters

```javascript
const chapters = await client.getMangaChapters(mangaId, {
  language: 'en',
  limit: 100,
  offset: 0,
  order: 'asc'
});
```

### Get Chapter Details

```javascript
const chapter = await client.getChapterDetails(chapterId);
```

### Get Chapter Images

```javascript
// Get image metadata
const imageData = await client.getChapterImages(chapterId);

// Build image URLs
const imageUrls = client.buildImageUrls(imageData, 'data'); // or 'data-saver'
```

## Rate Limiting

The MangaDex API has rate limits. This client includes:
- Built-in delays between requests (250ms)
- Error handling for 429 (Too Many Requests) responses
- Configurable timeout (10 seconds)

## Customization

### Change Search Query

Edit `index.js` and modify the `searchQuery` variable:

```javascript
const searchQuery = 'Your Manga Title Here';
```

### Adjust Chapter Limit

Modify the chapter fetch options:

```javascript
const chapters = await client.getMangaChapters(selectedManga.id, {
  language: 'en',
  limit: 50,  // Change this value
  order: 'asc'
});
```

### Change Language

Modify the language parameter:

```javascript
const chapters = await client.getMangaChapters(selectedManga.id, {
  language: 'ja',  // Japanese
  // or 'es', 'fr', 'de', etc.
});
```

## Error Handling

The client handles common errors:
- Network failures (automatic logging)
- API errors (status codes, error messages)
- Rate limiting (429 errors with helpful messages)
- Invalid IDs or missing data

## Documentation

For more information about the MangaDex API:
- [Official API Documentation](https://api.mangadex.org/docs/)
- [MangaDex Discord](https://discord.gg/mangadex)

## Notes

- **Do NOT send authentication headers** when fetching chapter images
- Base URLs for images expire after ~15 minutes
- Always report image download success/failures to the MangaDex@Home network
- Respect rate limits to avoid getting IP banned

## License

MIT

## Contributing

Feel free to submit issues or pull requests for improvements!
