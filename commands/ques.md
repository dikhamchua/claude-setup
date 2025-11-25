````markdown
## Prompt: Generate 10 Theory and Practical Questions from a Given File

### 1. Persona/Role
You are an **expert instructional designer and senior computer science educator**.  
You specialize in creating **structured, pedagogical question sets** that mix both **theory** and **practical exercises**.  
You have strong experience in **database systems, programming, and exam design**.

---

### 2. Context
The user will provide a **source file (document, notes, or article)** containing study material — for example, on SQL commands, programming concepts, or system design.  
Based on the content of that file, you will design **10 comprehensive questions** that test both **understanding (theory)** and **application (practice)**.

Each question must have:
- A **clear title** (the question itself)
- A **short explanation of the correct answer** in `"explain_question"` — *i.e., explain why the chosen answer(s) are correct*
- A **type** field (e.g., `"single_choice"`, `"multiple_choice"`, `"code_completion"`, `"short_answer"`)
- **4 options** for multiple-choice questions
- **Correct answers** listed by index (1-based)
- Use of **Markdown code formatting** for any code snippets or SQL statements

---

### 3. Task
Generate **10 questions** derived from the content of the provided file, following this structure:
1. Include a **mix of question types**:
   - ~5 theory questions (concepts, syntax, purpose)
   - ~5 practical or applied questions (predict output, write code, fix error)
2. Ensure all code examples use Markdown formatting:
   ```markdown
   ```sql
   SELECT * FROM Students;
````

````
3. Use **clear, educational phrasing** suitable for university-level learners.
4. Randomize the order of questions (not grouped by difficulty).
5. In `"explain_question"`, always **explain the reasoning behind the correct answer** — why it is correct, or why the other options are wrong.

---

### 4. Format
Output the result as a **JSON array** of 10 objects.  
Each object must follow the schema below:

```json
[
{
 "title": "What is the capital of France?",
 "explain_question": "The correct answer is Paris because it is the official capital and largest city of France, while the other options are capitals of different countries.",
 "type": "single_choice",
 "number_of_options": 4,
 "options": ["Paris", "London", "Berlin", "Madrid"],
 "correct_answers": [1]
}
]
````

---

### 5. Examples

#### Example 1 — Theory Question

```json
{
  "title": "What does the SQL command CREATE TABLE do?",
  "explain_question": "The correct answer is 'Creates a new table with defined columns' because the CREATE TABLE statement defines a new structure in the database. The other options describe DELETE, UPDATE, or INSERT behaviors, not CREATE.",
  "type": "single_choice",
  "number_of_options": 4,
  "options": [
    "Deletes a table from the database",
    "Creates a new table with defined columns",
    "Updates data in an existing table",
    "Copies data from one table to another"
  ],
  "correct_answers": [2]
}
```

#### Example 2 — Practical Question

```json
{
  "title": "Which of the following SQL statements correctly inserts a new record into the Students table?",
  "explain_question": "The correct answer is option 3 because the INSERT INTO statement must specify both the target columns and corresponding values. The other options either omit columns or use incorrect syntax.",
  "type": "single_choice",
  "number_of_options": 4,
  "options": [
    "INSERT Students VALUES ('John', 22);",
    "INSERT INTO Students ('John', 22);",
    "INSERT INTO Students (Name, Age) VALUES ('John', 22);",
    "ADD INTO Students (Name, Age) VALUES ('John', 22);"
  ],
  "correct_answers": [3]
}
```

---

### 6. Constraints

* **Number of questions:** Exactly 10
* **Language:** Same as the source file (English or Vietnamese)
* **Output format:** JSON only, no additional text
* **Code snippets:** Must use proper Markdown code blocks
* **Localtion:** File name must in format `question DD/MM/YYYY HH:MM:SS` Must in folder `output`, if not have, using bash to execute create folder
* **Question variety:** At least 3 conceptual, 3 syntax, 2 application, and 2 debugging-type questions
* **Indices:** `correct_answers` must use **1-based numbering**
* **No duplicate questions or overlapping content**
* **Every `"explain_question"` must clearly justify why the correct answer is correct**

---

**End of Prompt**

```

---

## JSON Encoding Rules for Quiz Application

```json
{
  "title": "JSON Encoding Rules for Quiz Application",
  "description": "Rules and guidelines for creating JSON files that work with the quiz application to avoid UTF-8 encoding errors",
  "problem": "Application throws 'Malformed UTF-8 characters, possibly incorrectly encoded' error when using special characters directly",
  "solution": "Use HTML entities to encode special characters",

  "html_entities_mapping": {
    "=": "&#61;",
    "+": "&#43;",
    "-": "&#45;",
    "%": "&#37;",
    "(": "&#40;",
    ")": "&#41;",
    "*": "&#42;",
    "/": "&#47;",
    "<": "&#60;",
    ">": "&#62;",
    "&": "&#38;",
    "!": "&#33;",
    "|": "&#124;",
    "^": "&#94;",
    "~": "&#126;",
    "[": "&#91;",
    "]": "&#93;",
    "{": "&#123;",
    "}": "&#125;"
  },

  "examples": {
    "before": "rear = (rear + 1) % capacity",
    "after": "rear &#61; &#40;rear &#43; 1&#41; &#37; capacity",

    "before_2": "front == rear",
    "after_2": "front &#61;&#61; rear",

    "before_3": "array[index]",
    "after_3": "array&#91;index&#93;"
  },

  "working_example": {
    "title": "Example question with special characters",
    "explain_question": "This is how to format questions with code",
    "type": "single_choice",
    "number_of_options": 4,
    "options": [
      "rear &#61; rear &#43; 1",
      "rear &#61; &#40;rear &#43; 1&#41; &#37; capacity",
      "Check if front &#61;&#61; rear",
      "array&#91;index&#93; &#43; 1"
    ],
    "correct_answers": [2]
  },

  "notes": [
    "Always use HTML entities for mathematical operators and brackets",
    "Regular text and alphanumeric characters do not need encoding",
    "The application will automatically decode HTML entities for display",
    "Use UTF-8 encoding without BOM when saving the file",
    "Test each file after creation to ensure it imports correctly"
  ],

  "what_did_not_work": [
    "Unicode escape sequences like \\u003d",
    "Markdown backticks like `code` for inline code with special characters",
    "Adding spaces between operators",
    "Using plain UTF-8 with special characters directly",
    "Using ensure_ascii=False in Python json.dump",
    "Using newline characters \\n and backticks ``` without HTML entities in code blocks"
  ],

  "what_works": [
    "HTML entities (&#XX;) for special characters",
    "Plain text for regular characters",
    "UTF-8 encoding with HTML entities",
    "Markdown code blocks with ```java syntax combined with HTML entities",
    "Inline code with backtick ` for text without special characters (variables, method names)"
  ],

  "markdown_support": {
    "description": "The application supports markdown rendering",
    "code_blocks": {
      "syntax": "```java\\ncode here\\n```",
      "important": "MUST use HTML entities for all special characters inside code blocks",
      "example": "```java\\nQueue&#60;Integer&#62; q &#61; new LinkedList&#60;&#62;&#40;&#41;;\\n```"
    },
    "inline_code": {
      "syntax": "`text here`",
      "safe_for": "Variable names, method names, simple text without special characters",
      "examples": [
        "`capacity = 3`",
        "`enqueue()`",
        "`poll()`",
        "`front` and `rear`"
      ],
      "warning": "Inline backtick can be used for display text, but ALL code in title/options MUST use HTML entities"
    }
  },

  "best_practices": [
    "Always encode ALL special characters in code blocks with HTML entities",
    "Use markdown code blocks (```java) for multi-line code",
    "Use inline backtick (`) for variable/method names in explanations only",
    "Split large question sets into smaller files (5 questions per file) for easier testing",
    "Test each file immediately after creation to catch encoding issues early",
    "Keep a copy of this encoding rules file in the project",
    "When in doubt, use HTML entities - they always work"
  ],

  "common_mistakes": [
    "Forgetting to encode = sign in assignments",
    "Not encoding parentheses () in method calls",
    "Missing encoding for brackets [] in array access",
    "Not encoding angle brackets <> in generics",
    "Forgetting to encode % in modulo operations",
    "Using backticks with special characters directly"
  ],

  "lessons_learned": [
    "Even with markdown support, HTML entities are REQUIRED for code",
    "Markdown rendering happens AFTER HTML entity decoding",
    "The application cannot handle raw special characters in JSON strings",
    "File splitting helps isolate and debug encoding issues",
    "Consistent encoding across all files prevents import errors"
  ]
}
```