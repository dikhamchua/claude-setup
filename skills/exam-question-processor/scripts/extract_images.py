"""
Extract text from exam question images using OpenRouter Vision API

This script processes images containing exam questions and extracts the text
using vision language models via OpenRouter API.

Features:
- Automatic retry with exponential backoff
- Progress tracking
- Error handling and logging
- Support for multiple image formats
- UTF-8 encoding for Vietnamese text
"""

import argparse
import base64
import io
import json
import re
import sys
import time
from pathlib import Path
from typing import Optional, Tuple

import requests

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def natural_sort_key(filename):
    """
    Sort key for natural ordering (q1, q2, ..., q10 instead of q1, q10, q2)

    Args:
        filename: File name or path

    Returns:
        List of string/int parts for natural sorting
    """
    parts = re.split(r'(\d+)', str(filename))
    return [int(part) if part.isdigit() else part for part in parts]


def encode_image_to_base64(image_path: Path) -> str:
    """
    Encode image file to base64 string

    Args:
        image_path: Path to image file

    Returns:
        Base64 encoded string
    """
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def extract_text_from_image(
    image_path: Path,
    api_key: str,
    model: str = "google/gemini-2.0-flash-exp:free",
    max_retries: int = 3,
    timeout: int = 30
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract text from image using OpenRouter Vision API with retry logic

    Args:
        image_path: Path to image file
        api_key: OpenRouter API key
        model: Model identifier (default: Gemini 2.0 Flash)
        max_retries: Maximum retry attempts (default: 3)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Tuple of (extracted_text, error_message)
        Returns (text, None) on success
        Returns (None, error) on failure
    """
    # Encode image
    try:
        base64_image = encode_image_to_base64(image_path)
    except Exception as e:
        return None, f"Failed to encode image: {str(e)}"

    # Determine MIME type
    extension = image_path.suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    mime_type = mime_types.get(extension, 'image/jpeg')

    # Prepare API request
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all text from this exam question image. Include question numbers, question text, and all answer options (A, B, C, D, etc.). Preserve the exact formatting and structure."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }

    # Retry loop
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)

            # Handle rate limiting
            if response.status_code == 429:
                wait_time = 60  # Wait 60 seconds for rate limit
                if attempt < max_retries - 1:
                    print(f"  ⏳ Rate limit hit. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    return None, "Rate limit exceeded after all retries"

            # Handle server errors with exponential backoff
            if response.status_code >= 500:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                if attempt < max_retries - 1:
                    print(f"  ⚠️  Server error {response.status_code}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    return None, f"Server error {response.status_code} after all retries"

            # Check for success
            response.raise_for_status()

            # Parse response
            result = response.json()

            # Extract text from response
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return content, None
            else:
                return None, "No content in API response"

        except requests.exceptions.Timeout:
            wait_time = 2 ** attempt
            if attempt < max_retries - 1:
                print(f"  ⏱️  Timeout. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                return None, "Request timeout after all retries"

        except requests.exceptions.RequestException as e:
            wait_time = 2 ** attempt
            if attempt < max_retries - 1:
                print(f"  ⚠️  Network error. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                return None, f"Network error after all retries: {str(e)}"

        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    return None, "Failed after all retries"


def save_extracted_text(text: str, output_path: Path, metadata: dict = None):
    """
    Save extracted text to file with optional metadata

    Args:
        text: Extracted text content
        output_path: Path to save file
        metadata: Optional metadata dictionary (image path, model, timestamp)
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        # Write metadata header if provided
        if metadata:
            f.write("=" * 80 + "\n")
            f.write("EXTRACTED TEXT METADATA\n")
            f.write("=" * 80 + "\n")
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")
            f.write("=" * 80 + "\n\n")

        # Write extracted text
        f.write(text)


def process_images_folder(
    input_folder: str,
    output_folder: str,
    api_key: str,
    model: str = "google/gemini-2.0-flash-exp:free",
    max_retries: int = 3,
    image_extensions: Tuple[str, ...] = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
):
    """
    Process all images in a folder

    Args:
        input_folder: Path to folder containing images
        output_folder: Path to save extracted text files
        api_key: OpenRouter API key
        model: Vision model to use
        max_retries: Maximum retry attempts per image
        image_extensions: Tuple of valid image extensions
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    # Validate input folder
    if not input_path.exists():
        print(f"❌ Error: Input folder not found: {input_folder}")
        return

    if not input_path.is_dir():
        print(f"❌ Error: Input path is not a directory: {input_folder}")
        return

    # Get all image files
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f"*{ext}"))

    # Natural sort
    image_files = sorted(image_files, key=natural_sort_key)

    if not image_files:
        print(f"⚠️  No images found in {input_folder}")
        return

    print(f"\n Found {len(image_files)} images in {input_folder}")
    print(f" Using model: {model}")
    print(f" Output folder: {output_folder}")
    print("=" * 80)

    # Process each image
    successful = 0
    failed = 0
    failed_files = []

    for idx, image_file in enumerate(image_files, 1):
        print(f"\n[{idx}/{len(image_files)}] Processing: {image_file.name}")

        # Extract text
        text, error = extract_text_from_image(
            image_file,
            api_key,
            model,
            max_retries
        )

        if error:
            print(f"  ❌ Failed: {error}")
            failed += 1
            failed_files.append((image_file.name, error))
            continue

        # Save extracted text
        output_filename = f"{image_file.stem}_extracted.txt"
        output_file = output_path / output_filename

        metadata = {
            "Image": image_file.name,
            "Model": model,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        save_extracted_text(text, output_file, metadata)
        print(f"  ✅ Saved: {output_filename}")
        successful += 1

    # Summary
    print("\n" + "=" * 80)
    print(" EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"✅ Successful: {successful}/{len(image_files)}")
    print(f"❌ Failed: {failed}/{len(image_files)}")

    if failed_files:
        print("\n⚠️  Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")

    print(f"\n Output saved to: {output_folder}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Extract text from exam question images using OpenRouter Vision API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python extract_images.py --input-folder images --api-key sk-or-xxx

  # Custom output folder and model
  python extract_images.py \\
    --input-folder images \\
    --output-folder extracted \\
    --api-key sk-or-xxx \\
    --model "openai/gpt-4-vision-preview"

  # Adjust retry settings
  python extract_images.py \\
    --input-folder images \\
    --api-key sk-or-xxx \\
    --max-retries 5
        """
    )

    parser.add_argument(
        '--input-folder',
        required=True,
        help='Path to folder containing exam question images'
    )

    parser.add_argument(
        '--output-folder',
        default='extracted_texts',
        help='Path to save extracted text files (default: extracted_texts)'
    )

    parser.add_argument(
        '--api-key',
        required=True,
        help='OpenRouter API key (get from https://openrouter.ai/keys)'
    )

    parser.add_argument(
        '--model',
        default='google/gemini-2.0-flash-exp:free',
        help='Vision model to use (default: google/gemini-2.0-flash-exp:free)'
    )

    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Maximum retry attempts per image (default: 3)'
    )

    args = parser.parse_args()

    # Validate API key format
    if not args.api_key.startswith('sk-or-'):
        print("⚠️  Warning: API key should start with 'sk-or-'")
        print("Get your key at: https://openrouter.ai/keys")

    # Process images
    process_images_folder(
        args.input_folder,
        args.output_folder,
        args.api_key,
        args.model,
        args.max_retries
    )


if __name__ == "__main__":
    main()
