---
name: exam-question-processor
description: Processes exam questions from images to create comprehensive study documents. Extracts text using OpenRouter Vision API, generates detailed answers with Vietnamese explanations, and exports to Markdown/HTML/PDF. Use when user needs to convert exam question images into structured documentation with solutions.
---

# Exam Question Processor

## Purpose

Automate the complete workflow of processing exam questions from images:
1. Extract text from question images using OpenRouter Vision API
2. Consolidate extracted questions into unified file
3. Generate detailed answers with bilingual format (English questions, Vietnamese explanations)
4. Include academic citations and references
5. Export to multiple formats (Markdown, HTML)

## When to Use This Skill

Activate when the user requests:
- "Process questions from images in folder"
- "Extract and document exam questions"
- "Create study guide from question images"
- "Generate solutions for exam questions"
- Mentions: converting images → text → documented answers
- Working with multiple-choice questions from exams

## Workflow

### Phase 1: Setup and Configuration

1. **Ask for API Key**
   - Prompt: "Please provide your OpenRouter API key for image text extraction:"
   - Store in memory for session (never persist to disk)
   - Validate format (starts with 'sk-or-')

2. **Check for Custom Prompt File**
   - Look for `temp_prompt.txt` in current directory
   - If found, use it for extraction
   - If not found, offer to use default prompt or create custom one
   - Template available at: `~/.claude/skills/exam-question-processor/templates/temp_prompt.txt`

3. **Determine Processing Mode**
   - Ask user: "Single exam or batch processing?"
   - **Single mode**: Process one exam/question set
   - **Batch mode**: Process multiple exam folders

4. **Get Input Path**
   - Ask for image folder path or parent folder (batch mode)
   - Validate path exists
   - Count images/folders to process

### Phase 2: Text Extraction

**Important:** If a `temp_prompt.txt` file exists in the current directory, the script will automatically use it. Otherwise, it uses the default prompt.

Run `python scripts/image_text_extractor.py` with parameters:
```bash
python scripts/image_text_extractor.py \
  --api-key <key> \
  --input-folder <path> \
  --output-folder extracted_texts \
  --file-pattern "*.png" \
  --max-retry-rounds 3 \
  --delay 1.0 \
  --prompt-file temp_prompt.txt
```

**Note:** The `--prompt-file` parameter defaults to `temp_prompt.txt`, so you can omit it if your prompt file has this name.

**Script behavior:**
- Uses `ImageTextExtractor` class with advanced retry queue system
- Processes each image (*.png, *.jpg, *.jpeg, *.webp)
- Sends to OpenRouter Vision API for OCR
- Automatic retry with multiple models: google/gemini-2.0-flash-001
- Failed extractions automatically added to retry queue
- Multiple retry rounds with progressive delays
- Saves: `q1_extracted.txt`, `q2_extracted.txt`, etc.
- Shows progress: `[1/50] Extracting q1.png... ✓`
- Generates summary report with success/failure statistics
- Logs errors but continues processing

**Retry Queue System:**
- **Round 1**: Process all images with model fallback
- **Round 2**: Retry failed images after 5s delay
- **Round 3**: Final retry after 10s delay
- Failed images saved as `*_error.txt` after all retries

**Error Handling:**
- **429 Rate Limit**: Auto-switch to different model
- **400 Bad Request**: Try alternative vision model
- **Network Error**: Exponential backoff (1s, 2s, 4s)
- **Timeout**: Retry up to 3 times per model

### Phase 3: Join Questions

Run `python scripts/join_questions.py`:
```bash
python scripts/join_questions.py \
  --input-folder extracted_texts \
  --output-folder joined_extract_text \
  --output-filename all_questions_joined.txt
```

**Script behavior:**
- Natural sort (q1, q2, ..., q9, q10, not q1, q10, q2)
- Add separators between questions
- Create header with metadata
- Output: `all_questions_joined.txt`

### Phase 4: Generate Solutions

Run `python scripts/generate_solutions.py`:
```bash
python scripts/generate_solutions.py \
  --input-file joined_extract_text/all_questions_joined.txt \
  --output-file joined_extract_text/DETAILED_SOLUTIONS.md \
  --language-mode bilingual \
  --include-citations
```

**Script behavior:**
- **Count total questions** from joined file first
- Parse each question from joined file
- For each question:
  - **Detect question type** (multiple-choice, essay, code)
  - If non-MCQ: Ask user "Skip, Process, or Stop?"
  - **Analyze question** using LLM reasoning
  - **Search web** for authoritative sources (if needed)
  - **Match citations** from citation database
  - **Generate answer** (keep English)
  - **Write explanation** in Vietnamese with:
    - Detailed reasoning
    - Code examples (if applicable)
    - Visual diagrams/tables
    - Step-by-step walkthrough
  - **Add references** from citation database
  - **Track progress**: Show "Processing question X of Y"

**Validation After Generation:**
- **Count generated solutions** in DETAILED_SOLUTIONS.md
- **Compare with total questions** from input file
- **Report statistics**:
  - Total questions found: X
  - Solutions generated: Y
  - Skipped (non-MCQ): Z
  - Missing/Failed: X - Y - Z
- **If missing questions detected**:
  - List question numbers that are missing
  - Ask user: "Continue generating missing questions?" or "Review manually?"
  - Re-run generation for missing questions only

**Output Format:**
```markdown
## QUESTION 1
**Question:**
[English question text]
- A. [Option A]
- B. [Option B]
- C. [Option C]
- D. [Option D]

### ✅ ĐÁP ÁN ĐÚNG: **[Correct answer]**

### 📖 GIẢI THÍCH:
[Vietnamese explanation with examples]

### 📚 TÀI LIỆU CHỨNG MINH:
- **Silberschatz - Database System Concepts**
  - Chapter X, Section Y.Z: "Title"
  - Page XXX
```

### Phase 5: Export to Multiple Formats

Run `python scripts/export_formats.py`:
```bash
python scripts/export_formats.py \
  --input joined_extract_text/DETAILED_SOLUTIONS.md \
  --output-html joined_extract_text/DETAILED_SOLUTIONS.html \
  --output-pdf joined_extract_text/DETAILED_SOLUTIONS.pdf
```

**Script behavior:**
- **HTML**: Apply CSS styling, add navigation, table of contents
- **PDF**: Convert HTML to PDF using WeasyPrint or similar
- Preserve all formatting, code blocks, tables
- Add page numbers, headers, footers to PDF

### Phase 6: Report Results

Display summary with validation:
```
✨ PROCESSING COMPLETE

📊 Summary:
- Total images found: 50
- Successfully extracted: 48
- Failed extractions: 2 (q15.png, q32.png)
- Total questions in joined file: 48
- Solutions generated: 48
- Non-MCQ skipped: 0
- Missing solutions: 0

✅ VALIDATION PASSED: All extracted questions have solutions!

📁 Output files created:
✓ extracted_texts/ (48 files)
✓ extracted_texts/summary_report.txt
✓ joined_extract_text/all_questions_joined.txt (48 questions)
✓ joined_extract_text/DETAILED_SOLUTIONS.md (48 solutions)
✓ joined_extract_text/DETAILED_SOLUTIONS.html
✓ joined_extract_text/DETAILED_SOLUTIONS.pdf

⏱️  Total time: 15m 32s
```

**If Validation Fails:**
```
⚠️  VALIDATION WARNING

📊 Summary:
- Total questions in joined file: 50
- Solutions generated: 47
- Missing solutions: 3

❌ Missing solutions for:
  - Question 15
  - Question 23
  - Question 47

Would you like to:
[1] Generate missing solutions now
[2] Review manually
[3] Continue anyway

Your choice:
```

## Batch Processing Mode

When user selects batch mode:

1. **Scan Parent Folder**
   - Identify subfolders containing images
   - Example structure:
     ```
     exams/
     ├── PE_14/
     │   ├── q1.png
     │   └── q2.png
     ├── PE_15/
     │   ├── q1.png
     │   └── q2.png
     ```

2. **Process Each Exam**
   - Run full workflow for each subfolder
   - Create separate output folders
   - Track progress across all exams

3. **Create Master Index**
   - Generate `index.md` linking to all exams
   - Summary table with stats for each exam

4. **Batch Report**
   ```
   ✨ BATCH PROCESSING COMPLETE

   📊 Overall Summary:
   - Total exams processed: 5
   - Total questions: 250
   - Average success rate: 96%

   📁 Exam Results:
   ✓ PE_14: 50 questions (100% success)
   ✓ PE_15: 50 questions (98% success)
   ✓ PE_16: 50 questions (94% success)
   ✓ PE_17: 50 questions (96% success)
   ✓ PE_18: 50 questions (92% success)

   ⏱️  Total time: 1h 15m
   ```

## Configuration

### API Models

Default model: `google/gemini-2.0-flash-001`

Alternative models (configurable in ImageTextExtractor class):
- `google/gemini-2.0-flash-exp:free`
- `google/gemini-flash-1.5-8b:free`
- `qwen/qwen-2-vl-7b-instruct:free`
- `meta-llama/llama-3.2-11b-vision-instruct:free`
- `openai/gpt-4o-mini`
- `openai/gpt-4o`

### Retry Strategy

- Max retry rounds: 3 (configurable via --max-retry-rounds)
- Model fallback: Automatic switch to next model on error
- Per-model retries: 3 attempts
- Backoff: Exponential (1s, 2s, 4s)
- Timeout per request: 120s
- Inter-round delay: Progressive (5s, 10s, 15s)
- Delay between requests: Configurable (default 1.0s)

### Language Settings

**Hardcoded** (not configurable):
- Question text: English
- Answer options: English
- Correct answer: English
- Explanations: Vietnamese
- References: English + Vietnamese titles

## Error Scenarios

### API Key Invalid
```
❌ Error: Invalid OpenRouter API key
Please check your key format (should start with 'sk-or-')
Get your key at: https://openrouter.ai/keys
```
**Action**: Re-prompt for API key

### All Retries Exhausted
```
⚠️  Failed to extract q15.png after 3 attempts
Error: 500 Server Error
```
**Action**: Log error, skip image, continue processing

### Non-Multiple-Choice Question Detected
```
❓ Question 25 appears to be an essay question:
"Explain the ACID properties of transactions..."

Options:
[1] Skip this question
[2] Process anyway (may not fit template)
[3] Stop processing

Your choice:
```
**Action**: Wait for user input, proceed accordingly

### Network Connection Lost
```
❌ Network error: Connection timeout
Retrying in 5 seconds... (Attempt 1/3)
```
**Action**: Auto-retry with backoff

### Missing Solutions Detected
```
⚠️  VALIDATION FAILED

After generating 47 solutions, validation found 3 questions without solutions:
- Question 15: Not found in output
- Question 23: Not found in output
- Question 47: Not found in output

This may be due to:
- Generation interrupted
- Questions were skipped
- Parsing errors

Recommended actions:
[1] Re-run generation for missing questions only
[2] Review input file for these question numbers
[3] Check if questions were intentionally skipped
```
**Action**: Ask user how to proceed, then re-run for missing questions if requested

## Examples

### Example 1: Single Exam Processing

**User**: "I have 50 exam question images in the folder 'PRO192_FE'. Can you process them?"

**Skill Response**:
1. ✅ "Please provide your OpenRouter API key:"
2. ✅ [User provides key]
3. ✅ "Checking for temp_prompt.txt... Found! Using custom extraction rules."
4. ✅ "Found 50 images in PRO192_FE/"
5. ✅ "Extracting text from images using ImageTextExtractor..."
   - Round 1: [1/50] Processing q1.png... ✓
   - Round 1: [2/50] Processing q2.png... ✓
   - Round 1 complete: 48/50 successful, 2 added to retry queue
   - Delay 5s before Round 2...
   - Round 2: [1/2] Processing q15.png... ✓
   - Round 2: [2/2] Processing q32.png... ✗ (failed)
   - Summary: 49/50 successful (98%)
6. ✅ "Joining questions..."
   - Found 49 questions in extracted_texts/
   - Created all_questions_joined.txt
7. ✅ "Generating solutions with Vietnamese explanations..."
   - Total questions to process: 49
   - [1/49] Generating solution for Question 1... ✓
   - [2/49] Generating solution for Question 2... ✓
   - ...
   - [49/49] Generating solution for Question 50... ✓
   - All solutions generated!
8. ✅ "Validating solutions..."
   - Total questions in input: 49
   - Solutions generated: 49
   - ✅ VALIDATION PASSED: All questions have solutions!
9. ✅ "Exporting to HTML and PDF..."
10. ✅ "✨ Complete! 49/50 questions processed. Files created."

### Example 2: Batch Processing

**User**: "Process all exam folders in my 'Exams' directory"

**Skill Response**:
1. ✅ "Please provide your OpenRouter API key:"
2. ✅ [User provides key]
3. ✅ "Found 5 exam folders with 250 total images"
4. ✅ "Processing PE_14... [50/50 extracted]"
5. ✅ "Processing PE_15... [49/50 extracted - 1 failed]"
6. ✅ [Continue for remaining exams]
7. ✅ "✨ Batch complete! Processed 5 exams, 245/250 questions."

### Example 3: Handling Validation Failure

**User**: "Process my exam questions"

**Skill Response**:
1. ✅ [Extraction complete: 50 questions]
2. ✅ [Joining complete: 50 questions]
3. ✅ [Generating solutions...]
   - [1/50] Question 1... ✓
   - [2/50] Question 2... ✓
   - ...
   - [47/50] Question 47... ✓
   - [48/50] Question 48... ✓
   - Generation complete
4. ⚠️  "Validating solutions..."
   - Total questions: 50
   - Solutions generated: 48
   - ❌ VALIDATION FAILED: 2 missing solutions
   - Missing: Question 15, Question 32
5. ⚠️  "Would you like to:
   [1] Generate missing solutions now
   [2] Review manually
   [3] Continue anyway"
6. ✅ [User chooses "1"]
7. ✅ "Generating missing solutions..."
   - [1/2] Question 15... ✓
   - [2/2] Question 32... ✓
8. ✅ "Re-validating..."
   - ✅ VALIDATION PASSED: All 50 questions have solutions!
9. ✅ "Exporting to HTML and PDF..."
10. ✅ "✨ Complete!"

### Example 4: Handling Non-MCQ

**User**: "Process my exam questions"

**Skill Response**:
1. ✅ [Processes first 24 MCQ questions normally]
2. ⚠️  "Question 25 is not multiple-choice. Skip, Process, or Stop?"
3. ✅ [User chooses "Process"]
4. ✅ [Adapts template for essay question]
5. ✅ [Continues with remaining questions]

## Templates

The skill uses templates from `templates/` folder:

- `question_template.md`: Format for individual questions
- `solution_template.md`: Format for detailed solutions
- `html_template.html`: HTML export styling

See templates for customization options.

## Citation Database

The skill references academic sources from `references/citation_database.json`:

- Silberschatz - Database System Concepts (7th Edition)
- Elmasri & Navathe - Fundamentals of Database Systems (7th Edition)
- Microsoft SQL Server Documentation
- Oracle Database Documentation

Citations are automatically matched based on topic keywords.

## Best Practices

1. **Before Starting**
   - Ensure images are clear and readable
   - Organize images in numbered sequence (q1.png, q2.png, ...)
   - Have OpenRouter API key ready
   - Prepare custom `temp_prompt.txt` if needed

2. **During Processing**
   - Monitor progress output
   - Note any failed extractions
   - Review non-MCQ questions when prompted
   - Watch for validation warnings

3. **After Completion - VALIDATION CHECKLIST**
   - ✅ **Count validation**: Compare questions vs solutions
   - ✅ Review DETAILED_SOLUTIONS.md for accuracy
   - ✅ Check failed extractions manually if any
   - ✅ Verify all question numbers are sequential
   - ✅ Ensure no duplicate question numbers
   - ✅ Verify PDF formatting looks correct
   - ✅ Spot-check Vietnamese explanations for clarity
   - ✅ Review summary_report.txt for statistics

4. **For Batch Processing**
   - Use consistent folder structure
   - Ensure each exam folder has unique name
   - Allocate sufficient time (15-20min per exam)
   - Run validation after each exam
   - Keep track of overall success rate

## Troubleshooting

**Issue**: "Rate limit exceeded"
**Solution**: Wait 60 seconds, script auto-retries

**Issue**: "Poor extraction quality"
**Solution**: Use higher quality images, try different model

**Issue**: "PDF generation failed"
**Solution**: Check WeasyPrint installation: `pip install weasyprint`

**Issue**: "Missing citations"
**Solution**: Add to `references/citation_database.json`

## Dependencies

Required Python packages (auto-checked by scripts):
```bash
pip install requests pillow markdown weasyprint beautifulsoup4
```

## Performance

- Single question extraction: ~2-5 seconds
- 50 questions extraction: ~5-10 minutes
- Solution generation: ~10-15 minutes
- Total per exam: ~15-25 minutes
- Batch (5 exams): ~1-2 hours

Times vary based on:
- API response speed
- Network connection
- Question complexity
- Model selected

## Notes

- API key is never saved to disk (memory only)
- All processing is local except API calls
- Supports Vietnamese UTF-8 encoding
- Compatible with Windows/Mac/Linux
- Preserves original images (read-only)
