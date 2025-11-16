# Exam Question Processor - Claude Code Skill

Automate the complete workflow of extracting exam questions from images, generating detailed solutions with Vietnamese explanations, and creating professional study documents.

## 🎯 What This Skill Does

1. **Extracts text** from exam question images using OpenRouter Vision API
2. **Consolidates** all questions into a unified file
3. **Generates detailed answers** with bilingual format (English questions, Vietnamese explanations)
4. **Adds academic citations** from database textbooks
5. **Exports** to multiple formats (Markdown, HTML, PDF)

## 📁 Skill Structure

```
~/.claude/skills/exam-question-processor/
├── SKILL.md                          # Main skill definition (Claude reads this)
├── README.md                         # This file
├── scripts/
│   ├── image_text_extractor.py      # Advanced OpenRouter vision extraction with retry queue
│   ├── join_questions.py            # Consolidate extracted texts
│   ├── generate_solutions.py        # Answer generation (placeholder)
│   └── export_formats.py            # HTML/PDF conversion
├── templates/
│   ├── solution_template.md         # Solution format template
│   └── temp_prompt.txt              # Custom extraction prompt template
└── references/
    └── citation_database.json       # Academic references
```

## 🚀 How to Use

### Method 1: Through Claude Code (Recommended)

Simply tell Claude:
```
"Process my exam questions from the images folder"
```

or

```
"I have 50 exam question images in folder 'PRO192_FE'. Extract and create solutions."
```

Claude will:
1. Activate the skill automatically
2. Ask for your OpenRouter API key
3. Walk you through the workflow
4. Generate all output files

### Method 2: Direct Script Usage

#### Step 1: Extract Text from Images

```bash
python ~/.claude/skills/exam-question-processor/scripts/image_text_extractor.py \
  --api-key sk-or-your-key-here \
  --input-folder /path/to/images \
  --output-folder extracted_texts \
  --file-pattern "*.png" \
  --max-retry-rounds 3 \
  --delay 1.0
```

**Features:**
- Advanced retry queue system with multiple rounds
- Automatic model fallback on errors
- Progress tracking with detailed statistics
- Summary report generation
- Custom prompt support via `temp_prompt.txt` file

**Custom Prompt:**
- Create a `temp_prompt.txt` file in your working directory
- The script will automatically use it for extraction
- Template available at `~/.claude/skills/exam-question-processor/templates/temp_prompt.txt`
- Supports advanced extraction rules (code formatting, watermark removal, etc.)

**Input:** Folder with images (q1.png, q2.jpg, etc.)
**Output:**
- `extracted_texts/q1_extracted.txt`, `q2_extracted.txt`, ...
- `extracted_texts/summary_report.txt`

#### Step 2: Join All Questions

```bash
python ~/.claude/skills/exam-question-processor/scripts/join_questions.py \
  --input-folder extracted_texts \
  --output-folder joined_extract_text \
  --output-filename all_questions_joined.txt
```

**Input:** `extracted_texts/` folder
**Output:** `joined_extract_text/all_questions_joined.txt`

#### Step 3: Generate Solutions

**Note:** This step currently requires running through Claude Code interactively, as it uses Claude's reasoning capabilities to generate Vietnamese explanations.

Tell Claude:
```
"Generate detailed solutions for all_questions_joined.txt with Vietnamese explanations"
```

**Process:**
1. Claude counts total questions in input file
2. Generates solutions one by one with progress tracking
3. **Automatic validation**: Compares generated count vs input count
4. If missing solutions detected:
   - Lists missing question numbers
   - Offers to re-generate missing ones
   - Re-validates after completion

**Output:** `joined_extract_text/DETAILED_SOLUTIONS.md`

**Validation ensures:**
- ✅ All questions have corresponding solutions
- ✅ No duplicate question numbers
- ✅ Sequential question numbering
- ✅ Complete coverage of input file

#### Step 4: Export to HTML/PDF

```bash
# Export to HTML
python ~/.claude/skills/exam-question-processor/scripts/export_formats.py \
  --input joined_extract_text/DETAILED_SOLUTIONS.md \
  --output-html joined_extract_text/DETAILED_SOLUTIONS.html

# Export to PDF (requires weasyprint)
python ~/.claude/skills/exam-question-processor/scripts/export_formats.py \
  --input joined_extract_text/DETAILED_SOLUTIONS.md \
  --output-html joined_extract_text/DETAILED_SOLUTIONS.html \
  --output-pdf joined_extract_text/DETAILED_SOLUTIONS.pdf
```

**Input:** `DETAILED_SOLUTIONS.md`
**Output:** `.html` and `.pdf` files

## 📋 Requirements

### Python Packages

```bash
pip install requests pillow markdown weasyprint
```

### API Keys

- **OpenRouter API Key**: Get from https://openrouter.ai/keys
  - Free tier available with `google/gemini-2.0-flash-exp:free` model
  - Supports multiple vision models (GPT-4V, Claude Sonnet, Gemini)

## 🎨 Output Format

The skill generates solutions in this bilingual format:

```markdown
## QUESTION 1
**Question:**
A person or persons responsible for the structure or schema of the database is
- A. A User
- B. A Coder
- C. A Customer
- D. A database administrator

### ✅ ĐÁP ÁN ĐÚNG: **D. A database administrator**

### 📖 GIẢI THÍCH:
**Database Administrator (DBA)** là người chịu trách nhiệm về:
1. **Database schema design** - Thiết kế cấu trúc database
2. **Physical database design** - Thiết kế vật lý
[... detailed Vietnamese explanation ...]

### 📚 TÀI LIỆU CHỨNG MINH:
- **Silberschatz - Database System Concepts (7th Edition)**
  - Chapter 1, Section 1.3: "Database Administrator"
  - Page 7-8
```

## ⚙️ Configuration

### Supported Vision Models

Edit the `vision_models` list in `image_text_extractor.py` ImageTextExtractor class:

**Free Models:**
- `google/gemini-2.0-flash-001` (default, paid but cheap)
- `google/gemini-2.0-flash-exp:free` (free tier, experimental)
- `google/gemini-flash-1.5-8b:free` (free tier)
- `qwen/qwen-2-vl-7b-instruct:free` (free tier)
- `meta-llama/llama-3.2-11b-vision-instruct:free` (free tier)

**Paid Models (Higher Accuracy):**
- `openai/gpt-4o-mini` (cheap, good accuracy)
- `openai/gpt-4o` (best accuracy)

### Retry Settings

Default configuration (configurable via command-line):
- Max retry rounds: 3 (--max-retry-rounds)
- Model fallback: Automatic on errors
- Per-model retries: 3 attempts
- Backoff: Exponential (1s, 2s, 4s)
- Timeout: 120s per request
- Inter-round delay: Progressive (5s, 10s, 15s)
- Delay between requests: 1.0s (--delay)

### Custom Extraction Prompt

The skill supports custom extraction prompts via `temp_prompt.txt`:

**Location:** Place in your working directory where you run the script

**Template:** `~/.claude/skills/exam-question-processor/templates/temp_prompt.txt`

**Features:**
- Custom extraction rules
- Code formatting instructions (Java, Python, C/C++, JavaScript)
- Watermark removal (e.g., "Kizspy", "FUO", "fuoverflow")
- Syntax preservation rules
- Output formatting instructions

**Example Rules:**
```
- Extract text exactly as it appears
- For code: preserve all syntax, indentation, comments
- Remove watermarks automatically
- Output only clean content
```

### Language Settings

**Hardcoded** (bilingual mode):
- Questions: English
- Answers: English
- Explanations: Vietnamese
- Code examples: English
- References: English + Vietnamese

## 📊 Performance

Typical processing times:
- Single question extraction: 2-5 seconds
- 50 questions extraction: 5-10 minutes
- Solution generation: 10-15 minutes (via Claude)
- HTML/PDF export: <1 minute
- **Total per exam: ~15-25 minutes**

Batch processing (5 exams, 250 questions):
- **Total time: ~1-2 hours**

## 🔧 Troubleshooting

### "Rate limit exceeded"
**Solution:** Script auto-retries after 60s. Free tier may have stricter limits.

### "Poor extraction quality"
**Solution:**
- Use higher resolution images
- Try different model (GPT-4V for better accuracy)
- Ensure images are clear and unobscured

### "PDF generation failed"
**Solution:**
```bash
pip install weasyprint
```

### "API key invalid"
**Solution:** Verify key starts with `sk-or-` and is active at https://openrouter.ai/keys

## 💡 Tips & Best Practices

### Before Starting
- ✅ Organize images in numbered sequence (q1.png, q2.png, ...)
- ✅ Ensure images are clear and readable
- ✅ Have OpenRouter API key ready
- ✅ Check available API credits/limits

### During Processing
- 📊 Monitor extraction progress
- ⚠️ Note any failed extractions for manual review
- 🔄 Be patient - quality extraction takes time

### After Completion
- ✅ Review DETAILED_SOLUTIONS.md for accuracy
- ✅ Check failed extractions manually
- ✅ Verify PDF formatting looks correct
- ✅ Spot-check Vietnamese explanations for clarity

### For Batch Processing
- 📁 Use consistent folder structure for all exams
- 🏷️ Give each exam folder a unique, descriptive name
- ⏱️ Allocate 15-20 minutes per exam set
- 💾 Monitor disk space (images + outputs can be large)

## 🌟 Examples

### Example 1: Single Exam

```
User: "I have 50 database questions in folder PRO192_FE. Please process them."

Claude:
✅ Skill activated: exam-question-processor
📋 Found 50 images
🔑 Please provide OpenRouter API key:

[User provides key]

📥 Extracting text from images... [Progress: 1/50, 2/50, ...]
✅ Extracted: 48/50 (2 failed)
📝 Joining questions...
✅ Created: all_questions_joined.txt
🎓 Generating solutions...
✅ Created: DETAILED_SOLUTIONS.md
📄 Exporting to HTML and PDF...
✅ Created: DETAILED_SOLUTIONS.html
✅ Created: DETAILED_SOLUTIONS.pdf

✨ Processing complete!
📊 Summary: 48 questions successfully processed
⚠️  Failed: q15.png, q32.png (retry recommended)
```

### Example 2: Batch Processing

```
User: "Process all exam folders in my 'Exams' directory"

Claude:
✅ Skill activated: exam-question-processor
📁 Found 5 exam folders (PE_14, PE_15, PE_16, PE_17, PE_18)
🔑 Please provide OpenRouter API key:

[Processing PE_14...]
✅ PE_14: 50/50 questions

[Processing PE_15...]
✅ PE_15: 49/50 questions (1 failed)

[... continues for all exams ...]

✨ Batch complete!
📊 Overall: 245/250 questions processed (98% success)
📁 Created master index.md with links to all exams
```

## 📚 Citation Database

The skill includes a curated database of academic references:

- **Silberschatz** - Database System Concepts (7th Edition)
- **Elmasri & Navathe** - Fundamentals of Database Systems (7th Edition)
- **Microsoft SQL Server Documentation**
- **Oracle Database Documentation**

Citations are automatically matched based on question topics (normalization, SQL, transactions, etc.)

## 🛠️ Customization

### Add New Citations

Edit `references/citation_database.json`:

```json
{
  "database_systems": {
    "YourTextbook": {
      "full_title": "Your Book Title",
      "edition": "1st Edition",
      "authors": ["Author Name"],
      "chapters": {
        "1": "Chapter Title"
      }
    }
  }
}
```

### Modify Templates

Edit `templates/solution_template.md` to customize output format.

### Change Models

Edit default model in scripts or pass via command line:

```bash
python extract_images.py ... --model "openai/gpt-4-vision-preview"
```

## 📖 Learn More

- **OpenRouter Documentation**: https://openrouter.ai/docs
- **Claude Code Skills Guide**: https://code.claude.com/docs/skills
- **Markdown Syntax**: https://www.markdownguide.org/

## 📝 License

This skill is provided as-is for educational and personal use.

## 🤝 Contributing

To improve this skill:
1. Test with different exam types
2. Report issues or enhancement ideas
3. Share improved templates or citations
4. Document edge cases and solutions

---

**Created by:** Claude Code
**Version:** 1.0.0
**Last Updated:** 2025-01-15
