"""
Image Text Extractor using OpenRouter Vision API
Extracts text from images using AI vision models
"""

import requests
import json
import os
import base64
from pathlib import Path
from typing import Optional, Dict, Any, List
import time
import argparse


class ImageTextExtractor:
    """
    Class để extract text từ ảnh sử dụng OpenRouter Vision API
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Khởi tạo Image Text Extractor

        Args:
            api_key: OpenRouter API key
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')

        if not self.api_key:
            raise ValueError(
                "API key không được cung cấp. "
                "Vui lòng truyền vào hoặc set biến môi trường OPENROUTER_API_KEY"
            )

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

        # Các model vision có sẵn trên OpenRouter (ưu tiên free hoặc giá rẻ)
        self.vision_models = [
            # "google/gemini-2.0-flash-exp:free",  # Free vision model - mạnh nhất
            "google/gemini-2.0-flash-001"
            # "google/gemini-flash-1.5-8b:free",   # Free backup
            # "qwen/qwen-2-vl-7b-instruct:free",   # Free alternative
            # "meta-llama/llama-3.2-11b-vision-instruct:free",  # Free alternative
            
            # "openai/gpt-4o-mini",  # Rẻ nhất trong GPT-4 vision
            # "openai/gpt-4o",
        ]

        self.model = self.vision_models[0]  # Dùng model đầu tiên làm mặc định

    def encode_image_to_base64(self, image_path: str) -> str:
        """
        Encode ảnh thành base64 string

        Args:
            image_path: Đường dẫn đến file ảnh

        Returns:
            Base64 encoded string
        """
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_image_mime_type(self, image_path: str) -> str:
        """
        Xác định MIME type của ảnh

        Args:
            image_path: Đường dẫn đến file ảnh

        Returns:
            MIME type string
        """
        ext = Path(image_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.bmp': 'image/bmp'
        }
        return mime_types.get(ext, 'image/jpeg')

    def extract_text_from_image(
        self,
        image_path: str,
        prompt: str = "Extract all text from this image.",
        temperature: float = 0.3,
        max_tokens: int = 4000,
        model: Optional[str] = None,
        retry_with_other_models: bool = True,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Extract text từ một ảnh với retry logic

        Args:
            image_path: Đường dẫn đến file ảnh
            prompt: Prompt yêu cầu extract text
            temperature: Độ ngẫu nhiên (0.0 - 1.0)
            max_tokens: Số token tối đa
            model: Model cụ thể (nếu không dùng mặc định)
            retry_with_other_models: Tự động thử model khác khi gặp lỗi
            max_retries: Số lần retry tối đa

        Returns:
            Dict chứa kết quả
        """
        # Encode ảnh một lần
        try:
            base64_image = self.encode_image_to_base64(image_path)
            mime_type = self.get_image_mime_type(image_path)
        except Exception as e:
            return {
                "success": False,
                "image_path": image_path,
                "error": f"Failed to read image: {str(e)}",
                "error_type": type(e).__name__
            }

        # Danh sách models để thử
        models_to_try = [model] if model else self.vision_models.copy()

        last_error = None
        last_error_type = None

        for attempt, current_model in enumerate(models_to_try, 1):
            try:
                # Chuẩn bị headers
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/image-text-extractor",
                    "X-Title": "Image Text Extractor"
                }

                # Chuẩn bị payload với vision format
                payload = {
                    "model": current_model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime_type};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }

                # Gửi request
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=120
                )

                response.raise_for_status()
                result = response.json()

                return {
                    "success": True,
                    "image_path": image_path,
                    "extracted_text": result["choices"][0]["message"]["content"],
                    "model": result.get("model"),
                    "usage": result.get("usage"),
                    "attempts": attempt
                }

            except requests.exceptions.HTTPError as e:
                last_error = str(e)
                last_error_type = type(e).__name__

                # Kiểm tra status code
                if hasattr(e.response, 'status_code'):
                    status_code = e.response.status_code

                    # 429 = Rate limit
                    if status_code == 429:
                        print(f"   ⚠️  Rate limit với {current_model}")
                        if retry_with_other_models and attempt < len(models_to_try):
                            print(f"   🔄 Chuyển sang model: {models_to_try[attempt]}")
                            time.sleep(2)  # Delay trước khi thử model khác
                            continue
                        else:
                            break

                    # 400 = Bad request - có thể model không hỗ trợ vision
                    elif status_code == 400:
                        print(f"   ⚠️  Model {current_model} không hỗ trợ hoặc bad request")
                        if retry_with_other_models and attempt < len(models_to_try):
                            print(f"   🔄 Chuyển sang model: {models_to_try[attempt]}")
                            time.sleep(1)
                            continue
                        else:
                            break

                    # Các lỗi khác
                    else:
                        break

            except requests.exceptions.RequestException as e:
                last_error = str(e)
                last_error_type = type(e).__name__

                # Timeout hoặc connection error - thử lại
                if attempt < max_retries:
                    print(f"   ⚠️  Lỗi kết nối, retry lần {attempt}...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    break

            except Exception as e:
                last_error = str(e)
                last_error_type = type(e).__name__
                break

        # Nếu tất cả đều thất bại
        return {
            "success": False,
            "image_path": image_path,
            "error": last_error,
            "error_type": last_error_type
        }

    def batch_extract_from_folder(
        self,
        folder_path: str,
        prompt: str = "Extract all text from this image.",
        output_folder: str = "extracted_texts",
        file_pattern: str = "*.jpeg",
        delay_seconds: float = 1.0,
        model: Optional[str] = None,
        skip_existing: bool = True,
        max_retry_rounds: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Extract text từ tất cả ảnh trong folder với retry queue system

        Args:
            folder_path: Đường dẫn đến folder chứa ảnh
            prompt: Prompt yêu cầu extract text
            output_folder: Folder để lưu kết quả
            file_pattern: Pattern của file ảnh (*.jpeg, *.png, etc.)
            delay_seconds: Delay giữa các request (tránh rate limit)
            model: Model cụ thể
            skip_existing: Bỏ qua file đã extract
            max_retry_rounds: Số lần retry queue tối đa

        Returns:
            List các kết quả
        """
        # Tạo output folder nếu chưa có
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)

        # Lấy danh sách ảnh
        folder = Path(folder_path)
        image_files = sorted(folder.glob(file_pattern))

        if not image_files:
            print(f"⚠️  Không tìm thấy ảnh nào trong {folder_path} với pattern {file_pattern}")
            return []

        # Lọc các file đã extract nếu skip_existing = True
        if skip_existing:
            files_to_process = []
            skipped_count = 0

            for image_file in image_files:
                output_file = output_path / f"{image_file.stem}_extracted.txt"
                if output_file.exists():
                    skipped_count += 1
                else:
                    files_to_process.append(image_file)

            if skipped_count > 0:
                print(f"⏭️  Bỏ qua {skipped_count} file đã extract")

            image_files = files_to_process

        if not image_files:
            print("✅ Tất cả file đã được extract!")
            return []

        print(f"📁 Tìm thấy {len(image_files)} ảnh cần xử lý")
        print(f"🤖 Sử dụng model: {model or self.model}")
        print(f"💾 Kết quả sẽ được lưu vào: {output_folder}")
        print(f"🔄 Max retry rounds: {max_retry_rounds}")
        print("=" * 80)

        all_results = []
        retry_queue = list(image_files)  # Queue chứa các file cần xử lý
        retry_round = 0

        while retry_queue and retry_round < max_retry_rounds:
            if retry_round > 0:
                print(f"\n{'=' * 80}")
                print(f"🔄 RETRY ROUND {retry_round}: {len(retry_queue)} ảnh còn lại")
                print(f"{'=' * 80}")

            current_batch = retry_queue.copy()
            retry_queue = []  # Clear queue để chứa các file lỗi mới

            for i, image_file in enumerate(current_batch, 1):
                total_processed = len(all_results) + i
                print(f"\n[{i}/{len(current_batch)}] (Round {retry_round + 1}) Đang xử lý: {image_file.name}")

                # Extract text với retry logic (thử tất cả models)
                result = self.extract_text_from_image(
                    image_path=str(image_file),
                    prompt=prompt,
                    model=model,
                    retry_with_other_models=True,
                    max_retries=3
                )

                # Hiển thị kết quả
                if result["success"]:
                    print(f"✅ Thành công!")
                    if "attempts" in result and result["attempts"] > 1:
                        print(f"   (Thành công sau {result['attempts']} lần thử)")

                    # Lưu kết quả vào file
                    output_file = output_path / f"{image_file.stem}_extracted.txt"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"Image: {image_file.name}\n")
                        f.write(f"Model: {result.get('model', 'N/A')}\n")
                        f.write(f"Retry Round: {retry_round + 1}\n")
                        f.write("=" * 80 + "\n\n")
                        f.write(result["extracted_text"])
                        f.write("\n\n" + "=" * 80 + "\n")
                        if "usage" in result:
                            f.write(f"Tokens used: {result['usage'].get('total_tokens', 'N/A')}\n")

                    print(f"💾 Đã lưu: {output_file.name}")

                    # Hiển thị preview
                    preview = result["extracted_text"][:200]
                    print(f"📄 Preview: {preview}...")

                    all_results.append(result)

                else:
                    print(f"❌ Lỗi: {result['error']}")

                    # Đưa vào retry queue nếu chưa hết retry rounds
                    if retry_round < max_retry_rounds - 1:
                        print(f"   🔄 Đưa vào retry queue")
                        retry_queue.append(image_file)
                    else:
                        print(f"   ⛔ Đã hết retry rounds, lưu lỗi")
                        # Lưu lỗi
                        error_file = output_path / f"{image_file.stem}_error.txt"
                        with open(error_file, 'w', encoding='utf-8') as f:
                            f.write(f"Image: {image_file.name}\n")
                            f.write(f"Error: {result['error']}\n")
                            f.write(f"Error Type: {result['error_type']}\n")
                            f.write(f"Retry Rounds: {retry_round + 1}\n")

                        all_results.append(result)

                # Delay để tránh rate limit
                if i < len(current_batch):
                    time.sleep(delay_seconds)

            retry_round += 1

            # Nếu còn file trong retry queue, delay lâu hơn trước khi retry
            if retry_queue:
                delay_time = 5 * retry_round  # Tăng delay theo số round
                print(f"\n⏸️  Delay {delay_time}s trước retry round tiếp theo...")
                time.sleep(delay_time)

        # Tạo summary report
        self._create_summary_report(all_results, output_path)

        # Hiển thị thống kê retry queue
        if retry_queue:
            print(f"\n⚠️  Còn {len(retry_queue)} ảnh không extract được sau {max_retry_rounds} rounds:")
            for img in retry_queue:
                print(f"   - {img.name}")

        return all_results

    def _create_summary_report(self, results: List[Dict[str, Any]], output_path: Path):
        """
        Tạo báo cáo tổng hợp

        Args:
            results: Danh sách kết quả
            output_path: Đường dẫn output folder
        """
        summary_file = output_path / "summary_report.txt"

        success_count = sum(1 for r in results if r["success"])
        fail_count = len(results) - success_count

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("IMAGE TEXT EXTRACTION - SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total images processed: {len(results)}\n")
            f.write(f"Successful: {success_count}\n")
            f.write(f"Failed: {fail_count}\n")
            f.write(f"Success rate: {success_count/len(results)*100:.1f}%\n\n")
            f.write("=" * 80 + "\n\n")

            # List failed images
            if fail_count > 0:
                f.write("FAILED IMAGES:\n")
                f.write("-" * 80 + "\n")
                for result in results:
                    if not result["success"]:
                        f.write(f"- {Path(result['image_path']).name}: {result['error']}\n")
                f.write("\n")

            # Total tokens used
            total_tokens = sum(
                r.get("usage", {}).get("total_tokens", 0)
                for r in results if r["success"]
            )
            f.write(f"Total tokens used: {total_tokens:,}\n")

        print("\n" + "=" * 80)
        print(f"✅ Hoàn thành! Đã xử lý {len(results)} ảnh")
        print(f"   - Thành công: {success_count}")
        print(f"   - Thất bại: {fail_count}")
        print(f"📊 Báo cáo chi tiết: {summary_file}")
        print("=" * 80)


def main():
    """
    Hàm main để chạy batch extraction
    """
    parser = argparse.ArgumentParser(
        description="Extract text from images using OpenRouter Vision API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with API key
  python image_text_extractor.py --api-key sk-or-xxx --input-folder images

  # Custom output and file pattern
  python image_text_extractor.py \\
    --api-key sk-or-xxx \\
    --input-folder images \\
    --output-folder extracted_texts \\
    --file-pattern "*.png"

  # With custom prompt file
  python image_text_extractor.py \\
    --api-key sk-or-xxx \\
    --input-folder images \\
    --prompt-file custom_prompt.txt
        """
    )

    parser.add_argument(
        '--api-key',
        required=False,
        help='OpenRouter API key (can also use OPENROUTER_API_KEY environment variable)'
    )

    parser.add_argument(
        '--input-folder',
        default='images',
        help='Path to folder containing images (default: images)'
    )

    parser.add_argument(
        '--output-folder',
        default='extracted_texts',
        help='Path to save extracted text files (default: extracted_texts)'
    )

    parser.add_argument(
        '--file-pattern',
        default='*.jpeg',
        help='File pattern to match (default: *.jpeg). Use *.png, *.jpg, etc.'
    )

    parser.add_argument(
        '--prompt-file',
        default='temp_prompt.txt',
        help='Path to file containing custom prompt (default: temp_prompt.txt)'
    )

    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay in seconds between requests (default: 1.0)'
    )

    parser.add_argument(
        '--max-retry-rounds',
        type=int,
        default=3,
        help='Maximum retry rounds for failed extractions (default: 3)'
    )

    args = parser.parse_args()

    print("=" * 80)
    print("IMAGE TEXT EXTRACTOR - BATCH PROCESSING")
    print("=" * 80)

    # Get API key from args or environment
    api_key = args.api_key or os.getenv('OPENROUTER_API_KEY')

    if not api_key:
        print("\nCảnh báo: Chưa thiết lập API key!")
        print("Vui lòng cung cấp API key bằng một trong hai cách:")
        print("  1. Sử dụng --api-key sk-or-xxx")
        print("  2. Set biến môi trường OPENROUTER_API_KEY")
        return

    # Validate API key format
    if not api_key.startswith('sk-or-'):
        print("\nCảnh báo: API key nên bắt đầu bằng 'sk-or-'")
        print("Get your key at: https://openrouter.ai/keys")

    # Read prompt from file if exists
    try:
        with open(args.prompt_file, 'r', encoding='utf-8') as f:
            custom_prompt = f.read().strip()
        print(f"\nĐã đọc prompt từ: {args.prompt_file}")
        print(f"Prompt: {custom_prompt[:100]}...")
    except FileNotFoundError:
        print(f"\nKhông tìm thấy {args.prompt_file}, sử dụng prompt mặc định")
        custom_prompt = "Extract all text from this image."

    # Initialize extractor with API key
    try:
        extractor = ImageTextExtractor(api_key=api_key)
    except ValueError as e:
        print(f"\nLỗi: {e}")
        return

    print(f"\nFolder ảnh: {args.input_folder}")
    print(f"Output folder: {args.output_folder}")
    print(f"File pattern: {args.file_pattern}")
    print(f"Delay: {args.delay}s")
    print(f"Max retry rounds: {args.max_retry_rounds}")

    # Run batch extraction
    print("\nBắt đầu xử lý...\n")

    results = extractor.batch_extract_from_folder(
        folder_path=args.input_folder,
        prompt=custom_prompt,
        output_folder=args.output_folder,
        file_pattern=args.file_pattern,
        delay_seconds=args.delay,
        max_retry_rounds=args.max_retry_rounds
    )

    print("\nHoàn thành tất cả!")


if __name__ == "__main__":
    main()
