#!/usr/bin/env python3
"""
Instagram Reel Image Scraper

This script takes an Instagram reel script, uses OpenAI to extract relevant
search terms, and downloads ~10 images from Pexels and Unsplash.
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from openai import OpenAI

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, rely on environment variables

# Configuration - Set these as environment variables or in .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Default download location
DOWNLOADS_DIR = Path.home() / "Downloads" / "reel-images"


def check_api_keys():
    """Verify all required API keys are set."""
    missing = []
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not PEXELS_API_KEY:
        missing.append("PEXELS_API_KEY")
    if not UNSPLASH_ACCESS_KEY:
        missing.append("UNSPLASH_ACCESS_KEY")
    
    if missing:
        print("❌ Missing API keys:")
        for key in missing:
            print(f"   - {key}")
        print("\nSet them as environment variables or in a .env file.")
        print("\nGet your API keys here:")
        print("  - OpenAI: https://platform.openai.com/api-keys")
        print("  - Pexels: https://www.pexels.com/api/new/")
        print("  - Unsplash: https://unsplash.com/developers")
        sys.exit(1)


def extract_search_terms(script: str) -> list[str]:
    """Use OpenAI to extract relevant image search terms from the script."""
    print("\n🤖 Analyzing script with AI...")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an expert at identifying visual concepts for image searches.
Given an Instagram reel script, extract 3-5 search terms that would find relevant, 
visually appealing images to accompany the content.

Rules:
- Focus on concrete, visual concepts (objects, scenes, emotions, actions)
- Avoid abstract concepts that don't photograph well
- Each term should be 1-3 words
- Return ONLY the search terms, one per line, no numbering or bullets"""
            },
            {
                "role": "user",
                "content": f"Extract image search terms from this Instagram reel script:\n\n{script}"
            }
        ],
        temperature=0.7,
        max_tokens=150
    )
    
    terms = response.choices[0].message.content.strip().split("\n")
    terms = [t.strip() for t in terms if t.strip()]
    
    print(f"   Found search terms: {', '.join(terms)}")
    return terms


def search_pexels(query: str, count: int = 5) -> list[dict]:
    """Search Pexels for images."""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": count, "orientation": "portrait"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        images = []
        for photo in data.get("photos", []):
            images.append({
                "url": photo["src"]["large2x"],
                "source": "pexels",
                "id": photo["id"],
                "photographer": photo.get("photographer", "Unknown")
            })
        return images
    except Exception as e:
        print(f"   ⚠️  Pexels search failed for '{query}': {e}")
        return []


def search_unsplash(query: str, count: int = 5) -> list[dict]:
    """Search Unsplash for images."""
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {"query": query, "per_page": count, "orientation": "portrait"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        images = []
        for photo in data.get("results", []):
            images.append({
                "url": photo["urls"]["regular"],
                "source": "unsplash",
                "id": photo["id"],
                "photographer": photo.get("user", {}).get("name", "Unknown")
            })
        return images
    except Exception as e:
        print(f"   ⚠️  Unsplash search failed for '{query}': {e}")
        return []


def download_image(image: dict, output_dir: Path, index: int) -> bool:
    """Download a single image to the output directory."""
    try:
        response = requests.get(image["url"], timeout=30)
        response.raise_for_status()
        
        # Determine file extension from content type
        content_type = response.headers.get("content-type", "image/jpeg")
        ext = "jpg" if "jpeg" in content_type else content_type.split("/")[-1]
        
        filename = f"{index:02d}_{image['source']}_{image['id']}.{ext}"
        filepath = output_dir / filename
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"   ⚠️  Failed to download image: {e}")
        return False


def create_output_directory(base_name: str = None) -> Path:
    """Create a timestamped output directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if base_name:
        # Sanitize the base name
        safe_name = "".join(c if c.isalnum() or c in "-_ " else "" for c in base_name)
        safe_name = safe_name.strip().replace(" ", "_")[:30]
        dir_name = f"{timestamp}_{safe_name}"
    else:
        dir_name = timestamp
    
    output_dir = DOWNLOADS_DIR / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def main():
    """Main entry point."""
    print("=" * 50)
    print("🖼️  Instagram Reel Image Scraper")
    print("=" * 50)
    
    # Check API keys
    check_api_keys()
    
    # Get script from user
    print("\nPaste your Instagram reel script below.")
    print("When done, press Enter twice (empty line) to continue:\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        except EOFError:
            break
    
    script = "\n".join(lines).strip()
    
    if not script:
        print("❌ No script provided. Exiting.")
        sys.exit(1)
    
    print(f"\n📝 Received script ({len(script)} characters)")
    
    # Extract search terms using AI
    search_terms = extract_search_terms(script)
    
    if not search_terms:
        print("❌ Could not extract search terms. Exiting.")
        sys.exit(1)
    
    # Search for images
    print("\n🔍 Searching for images...")
    all_images = []
    
    # Distribute searches across terms - aim for ~10 total images
    images_per_term = max(2, 10 // len(search_terms))
    
    for term in search_terms:
        print(f"   Searching: '{term}'")
        
        # Get images from both sources
        pexels_images = search_pexels(term, count=images_per_term)
        unsplash_images = search_unsplash(term, count=images_per_term)
        
        # Alternate between sources for variety
        for i in range(max(len(pexels_images), len(unsplash_images))):
            if i < len(pexels_images):
                all_images.append(pexels_images[i])
            if i < len(unsplash_images):
                all_images.append(unsplash_images[i])
    
    # Deduplicate and limit to ~10 images
    seen_ids = set()
    unique_images = []
    for img in all_images:
        img_id = f"{img['source']}_{img['id']}"
        if img_id not in seen_ids:
            seen_ids.add(img_id)
            unique_images.append(img)
            if len(unique_images) >= 10:
                break
    
    print(f"\n   Found {len(unique_images)} unique images")
    
    if not unique_images:
        print("❌ No images found. Try a different script.")
        sys.exit(1)
    
    # Create output directory
    first_term = search_terms[0] if search_terms else None
    output_dir = create_output_directory(first_term)
    
    # Download images
    print(f"\n📥 Downloading images to: {output_dir}")
    
    downloaded = 0
    for i, image in enumerate(unique_images, 1):
        print(f"   [{i}/{len(unique_images)}] Downloading from {image['source']}...", end=" ")
        if download_image(image, output_dir, i):
            print("✓")
            downloaded += 1
        else:
            print("✗")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"✅ Done! Downloaded {downloaded}/{len(unique_images)} images")
    print(f"📁 Location: {output_dir}")
    print("=" * 50)
    
    # Open the folder (macOS)
    if sys.platform == "darwin":
        os.system(f'open "{output_dir}"')


if __name__ == "__main__":
    main()
