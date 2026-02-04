# Instagram Reel Image Scraper

A Python script that takes your Instagram reel script, analyzes it with AI to find relevant search terms, and downloads ~10 high-quality images from Pexels and Unsplash.

## Features

- Uses OpenAI (GPT-4o-mini) to intelligently extract visual search terms from your script
- Searches both Pexels and Unsplash for variety
- Downloads portrait-oriented images (ideal for reels)
- Organizes images in timestamped folders
- Automatically opens the download folder when complete (macOS)

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Get your API keys (all free)

You'll need three API keys:

| Service | Free Tier | Get Key |
|---------|-----------|---------|
| **OpenAI** | Pay-per-use (~$0.01 per script) | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| **Pexels** | 200 requests/hour | [pexels.com/api/new](https://www.pexels.com/api/new/) |
| **Unsplash** | 50 requests/hour | [unsplash.com/developers](https://unsplash.com/developers) |

### 3. Set up your API keys

Create a `.env` file in this directory:

```bash
OPENAI_API_KEY=sk-your-openai-key-here
PEXELS_API_KEY=your-pexels-key-here
UNSPLASH_ACCESS_KEY=your-unsplash-access-key-here
```

Or export them in your terminal:

```bash
export OPENAI_API_KEY="sk-your-openai-key-here"
export PEXELS_API_KEY="your-pexels-key-here"
export UNSPLASH_ACCESS_KEY="your-unsplash-access-key-here"
```

## Usage

Run the script:

```bash
python image_scraper.py
```

Then paste your Instagram reel script and press Enter twice when done.

### Example

```
$ python image_scraper.py

==================================================
🖼️  Instagram Reel Image Scraper
==================================================

Paste your Instagram reel script below.
When done, press Enter twice (empty line) to continue:

Morning routines that changed my life:
1. Wake up at 5am before the chaos
2. 10 minutes of meditation
3. Cold shower to wake up your mind
4. Journal three things you're grateful for
5. Move your body - even just 10 minutes


📝 Received script (203 characters)

🤖 Analyzing script with AI...
   Found search terms: sunrise morning, meditation peaceful, cold shower, journaling notebook, morning exercise

🔍 Searching for images...
   Searching: 'sunrise morning'
   Searching: 'meditation peaceful'
   Searching: 'cold shower'
   Searching: 'journaling notebook'
   Searching: 'morning exercise'

   Found 10 unique images

📥 Downloading images to: /Users/you/Downloads/reel-images/20240115_143022_sunrise_morning
   [1/10] Downloading from pexels... ✓
   [2/10] Downloading from unsplash... ✓
   ...

==================================================
✅ Done! Downloaded 10/10 images
📁 Location: /Users/you/Downloads/reel-images/20240115_143022_sunrise_morning
==================================================
```

## Output

Images are saved to `~/Downloads/reel-images/` in timestamped folders:

```
~/Downloads/reel-images/
└── 20240115_143022_sunrise_morning/
    ├── 01_pexels_12345678.jpg
    ├── 02_unsplash_abc123.jpg
    ├── 03_pexels_87654321.jpg
    └── ...
```

## Troubleshooting

### "Missing API keys" error
Make sure your `.env` file is in the same directory as the script, or export the environment variables.

### "Rate limit exceeded" error
Wait a few minutes and try again. Pexels allows 200 requests/hour, Unsplash allows 50 requests/hour.

### No images found
Try a script with more concrete, visual concepts. Abstract ideas don't search well.

## License

MIT - Use freely for personal or commercial projects.
