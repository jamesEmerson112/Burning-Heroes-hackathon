# Video Generator

A Node.js client for the Higgsfield API to generate AI-powered videos from text, images, and reference materials.

## Features

- **Text-to-Video**: Generate videos from text prompts
- **Image-to-Video**: Animate static images with motion prompts
- **Soul Mode**: Create videos using multiple reference images for character consistency
- Automated status polling with progress tracking
- Error handling and detailed logging
- Environment-based configuration

## Prerequisites

- Node.js 18+ (recommended for native fetch support)
- A Higgsfield API key ([Get one here](https://higgsfieldapi.com))

## Installation

1. Navigate to the project directory:
```bash
cd video-generator
```

2. Install dependencies:
```bash
npm install
```

3. Configure your API key:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Higgsfield API key:
```
HIGGSFIELD_API_KEY=your_actual_api_key_here
```

## Usage

Run the example script to test all three generation modes:

```bash
npm start
```

This will execute:
1. Text-to-video generation with a cat playing with a ball
2. Image-to-video generation with a dog running in a park
3. Soul mode generation with multiple character references

## API Methods

### Text-to-Video

```javascript
import HiggsfieldAPI from './lib/HiggsfieldAPI.js';

const api = new HiggsfieldAPI(process.env.HIGGSFIELD_API_KEY);

const result = await api.generateTextToVideo('A cat playing with a ball', {
    duration: 10,
    resolution: '720p',
    aspect_ratio: '16:9',
    seed: 42
});
```

**Parameters:**
- `prompt` (required): Text description of the video
- `options` (optional):
  - `duration`: Video length in seconds (default: 5)
  - `resolution`: Video resolution (default: '720p')
  - `aspect_ratio`: Video aspect ratio (default: '16:9')
  - `seed`: Random seed for reproducibility

### Image-to-Video

```javascript
const result = await api.generateImageToVideo(
    'The dog runs in the park',
    'https://example.com/my-dog.jpg',
    {
        duration: 10,
        resolution: '720p',
        camera_fixed: false,
        seed: 123
    }
);
```

**Parameters:**
- `prompt` (required): Motion description
- `imageUrl` (required): URL of the source image
- `options` (optional):
  - `duration`: Video length in seconds (default: 5)
  - `resolution`: Video resolution (default: '720p')
  - `camera_fixed`: Lock camera position (default: false)
  - `seed`: Random seed for reproducibility

### Soul Mode

```javascript
const result = await api.generateSoulVideo(
    'A young woman and a monkey dancing together',
    [
        'https://example.com/woman-character.png',
        'https://example.com/monkey-character.png',
        'https://example.com/colorful-house.jpg'
    ]
);
```

**Parameters:**
- `prompt` (required): Scene description
- `referenceImageUrls` (required): Array of reference image URLs
- `options` (optional): Additional generation parameters

### Check Status

```javascript
const status = await api.getStatus(generationId);
console.log(status.status); // 'pending', 'in_queue', 'in_progress', 'completed', 'failed'
```

## Project Structure

```
video-generator/
├── package.json              # Project dependencies
├── .env.example             # Environment variable template
├── .env                     # Your API key (not committed)
├── .gitignore              # Git ignore patterns
├── README.md               # This file
├── lib/
│   └── HiggsfieldAPI.js    # API client class
└── index.js                # Example usage script
```

## Response Format

Successful generation request:
```json
{
    "success": true,
    "generation_id": "abc123",
    "status": "pending"
}
```

Status response:
```json
{
    "status": "completed",
    "video_url": "https://...",
    "generation_id": "abc123",
    "type": "text-to-video"
}
```

Error response:
```json
{
    "success": false,
    "error": "Error message",
    "status": 400
}
```

## Error Handling

The API client includes comprehensive error handling:
- Network errors (no response)
- API errors (non-2xx status codes)
- Request errors (malformed requests)

All errors are logged to the console with detailed information.

## Dependencies

- **axios** (^1.6.0): HTTP client for API requests
- **dotenv** (^16.3.0): Environment variable management

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For API-related issues, contact Higgsfield support at [higgsfieldapi.com](https://higgsfieldapi.com)

For project issues, please open a GitHub issue.
