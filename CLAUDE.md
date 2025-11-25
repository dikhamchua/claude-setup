### Core Responsibilities

#### 1. Code Implementation
- Before you start, delegate to `planner-researcher` agent to create a implementation plan with TODO tasks.
- Write clean, readable, and maintainable code
- Follow established architectural patterns
- Implement features according to specifications
- Handle edge cases and error scenarios

#### 2. Testing
- Write comprehensive unit tests
- Ensure high code coverage
- Test error scenarios
- Validate performance requirements
- Delegate to `tester` agent to run tests and analyze the summary report.
- If the `tester` agent reports failed tests, fix them follow the recommendations.

#### 3. Code Quality
- After finish implementation, delegate to `code-reviewer` agent to review code.
- Follow coding standards and conventions
- Write self-documenting code
- Add meaningful comments for complex logic
- Optimize for performance and maintainability

#### 4. Integration
- Follow the plan given by `planner-researcher` agent
- Ensure seamless integration with existing code
- Follow API contracts precisely
- Maintain backward compatibility
- Document breaking changes
- Delegate to `docs-manager` agent to update docs in `./docs` directory if any.

#### 5. Debugging
- When a user report bugs or issues on the server or a CI/CD pipeline, delegate to `debugger` agent to run tests and analyze the summary report.
- Read the summary report from `debugger` agent and implement the fix.
- Delegate to `tester` agent to run tests and analyze the summary report.
- If the `tester` agent reports failed tests, fix them follow the recommendations.

### Your Team (Subagents Team)

During the implementation process, you will delegate tasks to the following subagents based on their expertise and capabilities.

- **Planner & Researcher (`planner-researcher`)**: A senior technical lead specializing in searching on the internet, reading latest docs, understanding the codebase, designing scalable, secure, and maintainable software systems, and breaking down complex system designs into manageable, actionable tasks and detailed implementation instructions.

- **Tester (`tester`)**: A senior QA engineer specializing in running tests, unit/integration tests validation, ensuring high code coverage, testing error scenarios, validating performance requirements, validating build processes, and producing detailed summary reports with actionable tasks.

- **Debugger (`debugger`)**: A senior software engineer specializing in investigating production issues, analyzing system behavior, querying databases for diagnostic insights, examining table structures and relationships, collect and analyze logs in server infrastructure, read and collect logs in the CI/CD pipelines (github actions), running tests, and developing optimizing solutions for performance bottlenecks, and creating comprehensive summary reports with actionable recommendations.


- **Code Reviewer (`code-reviewer`)**: A senior software engineer specializing in comprehensive code quality assessment and best practices enforcement, performing code linting and TypeScript type checking, validating build processes and deployment readiness, conducting performance reviews for optimization opportunities, and executing security audits to identify and mitigate vulnerabilities. Read the original implementation plan file in `./plans` directory and review the completed tasks, make sure everything is implemented properly as per the plan. Finally producing detailed summary reports with actionable recommendations.

---

## Development Rules

### General
- Use `context7` mcp tools for exploring latest docs of plugins/packages
- Use `senera` mcp tools for semantic retrieval and editing capabilities
- Use `planner-researcher` agent to plan for the implementation plan.
- Use `tester` agent to run tests and analyze the summary report.
- Use `debugger` agent to collect logs in server or github actions to analyze the summary report.
- Use `code-reviewer` agent to review code.
- Use `docs-manager` agent to update docs in `./docs` directory if any.

### Code Quality Guidelines
- Don't be too harsh on code linting
- Prioritize functionality and readability over strict style enforcement and code formatting
- Use reasonable code quality standards that enhance developer productivity
- Use try catch error handling

---

## Serena MCP Tools - Quick Reference

### Core Principles
1. **Read only what you need** - Don't read entire files
2. **Use symbolic tools first** - Start with overview before full files
3. **Step-by-step exploration** - Gather information incrementally

### Essential Tools

**Code Discovery:**
- `list_dir(relative_path=".", recursive=true)` - Explore directory structure
- `find_file(file_mask="*.java", relative_path="src")` - Find files by pattern
- `get_symbols_overview(relative_path="file.java")` - **ALWAYS use before reading full file**
- `find_symbol(name_path="Class/method", include_body=true)` - Get specific symbol with code
- `find_referencing_symbols(name_path="Class/method", relative_path="file.java")` - Find usages

**Code Editing:**
- `replace_symbol_body(name_path="Class/method", relative_path="file.java", body="...")` - Replace method/function
- `insert_after_symbol(name_path="LastMethod", relative_path="file.java", body="...")` - Add after symbol
- `insert_before_symbol(name_path="FirstClass", relative_path="file.java", body="...")` - Add before symbol

**Pattern Search:**
- `search_for_pattern(substring_pattern="regex", relative_path="src")` - Regex-based search

### Workflow Examples

**Reading Code:**
```
1. list_dir(relative_path=".", recursive=false)
2. get_symbols_overview(relative_path="target_file.java")
3. find_symbol(name_path="ClassName", include_body=false, depth=1)
4. find_symbol(name_path="ClassName/methodName", include_body=true)
```

**Editing Code:**
```
1. find_symbol(name_path="Class/method", include_body=true)
2. find_referencing_symbols(name_path="Class/method", relative_path="file.java")
3. replace_symbol_body(name_path="Class/method", relative_path="file.java", body="...")
```

### Best Practices
- ✅ Start with `get_symbols_overview` for any new file
- ✅ Use `find_symbol` for targeted reading
- ✅ Check references before editing with `find_referencing_symbols`
- ✅ Set `include_body=false` when you only need metadata
- ✅ Use `depth=1` to see children without full bodies
- ❌ Don't read entire files when you only need one method
- ❌ Don't edit without checking references first