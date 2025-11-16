# Quick Start Guide - Exam Question Processor

## ⚡ Fastest Way to Use

### Option 1: Through Claude Code (Easiest)

Just tell Claude in natural language:

```
"Process my exam questions from folder PRO192_FE"
```

or

```
"I have 50 exam images in images/ folder. Extract text and create solutions."
```

Claude will automatically:
1. Activate this skill
2. Ask for your API key
3. Guide you through the process
4. Create all output files

### Option 2: Command Line

```bash
# 1. Extract text (get API key from https://openrouter.ai/keys)
python ~/.claude/skills/exam-question-processor/scripts/extract_images.py \
  --input-folder your_images_folder \
  --api-key sk-or-your-key-here

# 2. Join questions
python ~/.claude/skills/exam-question-processor/scripts/join_questions.py \
  --input-folder extracted_texts

# 3. Generate solutions (use Claude Code)
# Tell Claude: "Generate solutions for joined_extract_text/all_questions_joined.txt"

# 4. Export to HTML/PDF
python ~/.claude/skills/exam-question-processor/scripts/export_formats.py \
  --input joined_extract_text/DETAILED_SOLUTIONS.md \
  --output-html joined_extract_text/DETAILED_SOLUTIONS.html \
  --output-pdf joined_extract_text/DETAILED_SOLUTIONS.pdf
```

## 📋 Prerequisites

```bash
# Install required packages
pip install requests pillow markdown weasyprint

# Get OpenRouter API key
# Visit: https://openrouter.ai/keys
```

## 📁 Input Format

Your images folder should look like:
```
images/
├── q1.png
├── q2.jpg
├── q3.webp
└── ...
```

Supported formats: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`

## 📤 Output Files

After processing, you'll get:
```
extracted_texts/           # Individual extracted files
  ├── q1_extracted.txt
  ├── q2_extracted.txt
  └── ...

joined_extract_text/       # Consolidated outputs
  ├── all_questions_joined.txt     # All questions merged
  ├── DETAILED_SOLUTIONS.md        # Solutions with Vietnamese explanations
  ├── DETAILED_SOLUTIONS.html      # HTML version
  └── DETAILED_SOLUTIONS.pdf       # PDF version
```

## 🎯 Example Workflow

**You have:** Folder with 50 exam question images

**Steps:**
1. Open Claude Code
2. Say: "Process exam questions from folder PRO192_FE"
3. Provide OpenRouter API key when asked
4. Wait ~15-20 minutes
5. Get Markdown + HTML + PDF with complete solutions!

## 🔧 Configuration

### Change Vision Model

Default: `google/gemini-2.0-flash-exp:free` (Free tier)

To use different model:
```bash
python extract_images.py ... --model "openai/gpt-4-vision-preview"
```

Available models:
- `google/gemini-2.0-flash-exp:free` - Free, fast, good accuracy
- `openai/gpt-4-vision-preview` - Paid, best accuracy
- `anthropic/claude-3-5-sonnet-20241022` - Paid, great for complex questions

### Batch Process Multiple Exams

Tell Claude:
```
"Process all exam folders in my Exams directory"
```

Your folder structure:
```
Exams/
├── PE_14/
│   ├── q1.png
│   └── ...
├── PE_15/
│   ├── q1.png
│   └── ...
└── ...
```

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Rate limit error | Wait 60s, script retries automatically |
| Poor extraction | Use higher quality images or try GPT-4V model |
| PDF fails | Install: `pip install weasyprint` |
| API key invalid | Get new key at https://openrouter.ai/keys |

## 💡 Pro Tips

- ✅ Use clear, high-resolution images
- ✅ Number images sequentially (q1, q2, q3...)
- ✅ Check free tier limits before starting large batches
- ✅ Review extracted text before generating solutions
- ✅ Keep original images (process is non-destructive)

## 📚 Full Documentation

See `README.md` for complete documentation.

---

**Ready to start?**

Try: "Hey Claude, process my exam questions from the images folder!"
