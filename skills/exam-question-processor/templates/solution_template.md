## QUESTION {{question_number}}
**Question:**
{{question_text}}
{{#if options}}
{{#each options}}
- {{this}}
{{/each}}
{{/if}}

### ✅ ĐÁP ÁN ĐÚNG: **{{correct_answer}}**

### 📖 GIẢI THÍCH:
{{explanation_vietnamese}}

{{#if code_examples}}
**Ví dụ Code:**
```{{code_language}}
{{code_examples}}
```
{{/if}}

{{#if references}}
### 📚 TÀI LIỆU CHỨNG MINH:
{{#each references}}
- **{{this.source}}**
  - {{this.chapter}}: "{{this.title}}"
  - Page {{this.page}}
{{/each}}
{{/if}}

---
