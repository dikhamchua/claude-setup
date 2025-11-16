"""
Join extracted question texts into a single consolidated file

This script combines all extracted text files into one unified document
with proper formatting and metadata.

Features:
- Natural sorting (q1, q2, ..., q10 not q1, q10, q2)
- Configurable separators
- Metadata removal options
- Multiple output modes
"""

import argparse
import re
from pathlib import Path
from typing import List


def natural_sort_key(filename):
    """
    Sort key for natural ordering

    Args:
        filename: File name or path

    Returns:
        List of string/int parts for natural sorting
    """
    parts = re.split(r'(\d+)', str(filename))
    return [int(part) if part.isdigit() else part for part in parts]


def extract_text_content(content: str, include_metadata: bool = False) -> str:
    """
    Extract main text content, optionally removing metadata header

    Args:
        content: File content
        include_metadata: If True, keep metadata header

    Returns:
        Extracted content
    """
    if include_metadata:
        return content

    # Remove metadata header (between first two === lines)
    lines = content.split('\n')

    # Find metadata boundaries
    separator_indices = []
    for idx, line in enumerate(lines):
        if '=' * 40 in line:
            separator_indices.append(idx)
            if len(separator_indices) == 2:
                break

    # If metadata found, skip it
    if len(separator_indices) >= 2:
        text_start = separator_indices[1] + 1
        return '\n'.join(lines[text_start:]).strip()

    return content.strip()


def join_extracted_files(
    input_folder: str,
    output_folder: str,
    output_filename: str = "all_questions_joined.txt",
    include_separator: bool = True,
    include_metadata: bool = False,
    pattern: str = "*_extracted.txt"
):
    """
    Join all extracted text files into single document

    Args:
        input_folder: Folder containing extracted text files
        output_folder: Folder to save joined file
        output_filename: Name of output file
        include_separator: Add separators between questions
        include_metadata: Keep metadata headers from individual files
        pattern: Glob pattern for matching files
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    # Validate input
    if not input_path.exists():
        print(f" Error: Input folder not found: {input_folder}")
        return

    # Get all extracted files
    extracted_files = list(input_path.glob(pattern))

    if not extracted_files:
        print(f"  No extracted files found in {input_folder}")
        return

    # Natural sort
    extracted_files = sorted(extracted_files, key=natural_sort_key)

    print(f"\n Found {len(extracted_files)} extracted files")
    print(f" Output: {output_folder}/{output_filename}")
    print("=" * 80)

    # Create output folder
    output_path.mkdir(parents=True, exist_ok=True)

    # Create joined file
    output_file = output_path / output_filename

    with open(output_file, 'w', encoding='utf-8') as out_f:
        # Write header
        out_f.write("=" * 80 + "\n")
        out_f.write("JOINED EXTRACTED TEXTS - ALL QUESTIONS\n")
        out_f.write("=" * 80 + "\n")
        out_f.write(f"Total files: {len(extracted_files)}\n")
        out_f.write(f"Source folder: {input_folder}\n")
        out_f.write("=" * 80 + "\n\n")

        # Process each file
        for idx, file_path in enumerate(extracted_files, 1):
            print(f"[{idx}/{len(extracted_files)}] Processing: {file_path.name}")

            try:
                # Read file
                with open(file_path, 'r', encoding='utf-8') as in_f:
                    content = in_f.read()

                # Extract question number from filename
                match = re.search(r'q(\d+)', file_path.name, re.IGNORECASE)
                question_num = match.group(1) if match else str(idx)

                # Write separator header
                if include_separator:
                    out_f.write("\n" + "=" * 80 + "\n")
                    out_f.write(f"QUESTION {question_num}\n")
                    out_f.write("=" * 80 + "\n\n")

                # Extract and write content
                text_content = extract_text_content(content, include_metadata)
                out_f.write(text_content)
                out_f.write("\n\n")

            except Exception as e:
                print(f"    Error reading file: {str(e)}")
                continue

        # Write footer
        out_f.write("\n" + "=" * 80 + "\n")
        out_f.write("END OF JOINED FILE\n")
        out_f.write("=" * 80 + "\n")

    print("\n" + "=" * 80)
    print(f" Successfully joined {len(extracted_files)} files")
    print(f" Output file: {output_file}")
    print(f" Size: {output_file.stat().st_size:,} bytes")
    print("=" * 80)


def create_separate_clean_files(
    input_folder: str,
    output_folder: str,
    pattern: str = "*_extracted.txt"
):
    """
    Create separate clean files (no metadata) for each question

    Args:
        input_folder: Folder containing extracted text files
        output_folder: Folder to save clean files
        pattern: Glob pattern for matching files
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    # Validate input
    if not input_path.exists():
        print(f" Error: Input folder not found: {input_folder}")
        return

    # Get all extracted files
    extracted_files = list(input_path.glob(pattern))

    if not extracted_files:
        print(f"  No extracted files found in {input_folder}")
        return

    # Natural sort
    extracted_files = sorted(extracted_files, key=natural_sort_key)

    print(f"\n Creating {len(extracted_files)} clean files")
    print("=" * 80)

    # Create output folder
    output_path.mkdir(parents=True, exist_ok=True)

    # Process each file
    for idx, file_path in enumerate(extracted_files, 1):
        print(f"[{idx}/{len(extracted_files)}] Processing: {file_path.name}")

        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as in_f:
                content = in_f.read()

            # Extract question number
            match = re.search(r'q(\d+)', file_path.name, re.IGNORECASE)
            question_num = match.group(1) if match else str(idx)

            # Extract clean content (no metadata)
            clean_content = extract_text_content(content, include_metadata=False)

            # Save clean file
            output_file = output_path / f"Q{question_num}_clean.txt"
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(clean_content)

            print(f"   Created: Q{question_num}_clean.txt")

        except Exception as e:
            print(f"    Error: {str(e)}")
            continue

    print("\n Successfully created clean files")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Join extracted question texts into single file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic join (default settings)
  python join_questions.py --input-folder extracted_texts

  # Custom output location and filename
  python join_questions.py \\
    --input-folder extracted_texts \\
    --output-folder joined \\
    --output-filename all_questions.txt

  # Include metadata and remove separators
  python join_questions.py \\
    --input-folder extracted_texts \\
    --include-metadata \\
    --no-separator

  # Create separate clean files only
  python join_questions.py \\
    --input-folder extracted_texts \\
    --mode separate
        """
    )

    parser.add_argument(
        '--input-folder',
        required=True,
        help='Path to folder containing extracted text files'
    )

    parser.add_argument(
        '--output-folder',
        default='joined_extract_text',
        help='Path to save output files (default: joined_extract_text)'
    )

    parser.add_argument(
        '--output-filename',
        default='all_questions_joined.txt',
        help='Name of joined output file (default: all_questions_joined.txt)'
    )

    parser.add_argument(
        '--mode',
        choices=['join', 'separate', 'both'],
        default='join',
        help='Processing mode: join, separate, or both (default: join)'
    )

    parser.add_argument(
        '--no-separator',
        action='store_true',
        help='Do not add separators between questions'
    )

    parser.add_argument(
        '--include-metadata',
        action='store_true',
        help='Keep metadata headers from individual files'
    )

    parser.add_argument(
        '--pattern',
        default='*_extracted.txt',
        help='Glob pattern for matching files (default: *_extracted.txt)'
    )

    args = parser.parse_args()

    # Process based on mode
    if args.mode in ['join', 'both']:
        print("\n Mode: Join all files")
        join_extracted_files(
            args.input_folder,
            args.output_folder,
            args.output_filename,
            include_separator=not args.no_separator,
            include_metadata=args.include_metadata,
            pattern=args.pattern
        )

    if args.mode in ['separate', 'both']:
        print("\n Mode: Create separate clean files")
        create_separate_clean_files(
            args.input_folder,
            args.output_folder,
            pattern=args.pattern
        )

    print("\n Processing complete!")


if __name__ == "__main__":
    main()
