### Core Responsibilities

#### 1. Code Implementation
- Before you start, delegate to `planner-researcher` agent to create a implementation plan with TODO tasks in `./plans` directory.
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

## Serena MCP Tools Guide

### Overview
Serena MCP provides semantic code analysis and editing tools for efficient codebase navigation and modification. These tools work at the **symbol level** (classes, methods, functions) rather than line-by-line, enabling intelligent code operations.

### Core Principles
1. **Read only what you need** - Don't read entire files unless necessary
2. **Use symbolic tools first** - Start with overview and symbol search before reading full files
3. **Step-by-step exploration** - Gather information incrementally
4. **Leverage caching** - Serena caches parsed symbols for fast access

---

### Tool Categories

#### 1. Project Management Tools

##### `activate_project`
**Purpose:** Activate a Serena project

**When to use:**
- First time working with a codebase
- Switching between different projects

**Example:**
```
activate_project(project="C:\\Users\\dell\\OneDrive - vinhdeptrai\\4user.net\\LAB211 02")
```

##### `get_current_config`
**Purpose:** View current Serena configuration

**When to use:**
- Check active project
- See available tools and memories
- Debug Serena setup issues

##### `check_onboarding_performed`
**Purpose:** Check if project has been onboarded

**When to use:**
- After activating a new project
- Before starting work on unfamiliar codebase

##### `onboarding`
**Purpose:** Start project onboarding process

**When to use:**
- First time analyzing a codebase
- Need to create project memories
- Building understanding of new project

---

#### 2. Memory Management Tools

##### `write_memory`
**Purpose:** Save information about the project for future reference

**When to use:**
- After onboarding to document project structure
- Document important patterns and conventions
- Save architectural decisions
- Record frequently used commands

**Parameters:**
- `memory_name`: Descriptive filename (e.g., "project_overview.md")
- `content`: Markdown-formatted content

**Example:**
```
write_memory(
    memory_name="coding_standards.md",
    content="# Coding Standards\n\n- Use camelCase for variables..."
)
```

##### `read_memory`
**Purpose:** Read saved project information

**When to use:**
- Need to recall project-specific information
- Check coding conventions
- Review architectural patterns
- Only if relevant to current task

**Example:**
```
read_memory(memory_file_name="project_overview.md")
```

##### `list_memories`
**Purpose:** List all available memory files

**When to use:**
- See what information is available
- Find relevant memories for current task

##### `delete_memory`
**Purpose:** Remove outdated memory file

**When to use:**
- User explicitly requests deletion
- Information is no longer relevant/correct

---

#### 3. Code Discovery Tools

##### `list_dir`
**Purpose:** List files and directories

**When to use:**
- Understanding project structure
- Finding source directories
- Locating configuration files
- **First step** when exploring new codebase

**Parameters:**
- `relative_path`: Directory to list (use "." for project root)
- `recursive`: true for subdirectories, false for single level
- `skip_ignored_files`: true to skip gitignored files

**Example:**
```
list_dir(relative_path=".", recursive=false)
list_dir(relative_path="src", recursive=true)
```

##### `find_file`
**Purpose:** Find files matching a pattern

**When to use:**
- Looking for specific files by name
- Finding all files of certain type
- Locating configuration files

**Parameters:**
- `file_mask`: Pattern with wildcards (e.g., "*.java", "Main.java", "pom.xml")
- `relative_path`: Directory to search (use "." for entire project)

**Example:**
```
find_file(file_mask="*.java", relative_path="src")
find_file(file_mask="Main.java", relative_path=".")
find_file(file_mask="pom.xml", relative_path=".")
```

##### `get_symbols_overview`
**Purpose:** Get high-level overview of symbols in a file

**When to use:**
- **ALWAYS use this before reading full file**
- First step when exploring a new file
- Understanding file structure
- Finding classes, methods, fields without reading bodies

**Parameters:**
- `relative_path`: Path to the file

**Returns:** List of top-level symbols (classes, interfaces, enums)

**Example:**
```
get_symbols_overview(relative_path="src/controller/Main.java")
```

**Output example:**
```
[
  {"name_path": "controller", "kind": 4},  # Package
  {"name_path": "Main", "kind": 5}         # Class (kind 5)
]
```

##### `find_symbol`
**Purpose:** Find and retrieve symbol information

**When to use:**
- Looking for specific class, method, or field
- Need symbol details with/without body
- Want to see symbol's children (methods of a class)

**Parameters:**
- `name_path`: Symbol path pattern (see Name Path Patterns below)
- `relative_path`: File or directory to search (optional, searches entire project if omitted)
- `include_body`: true to get source code, false for metadata only
- `depth`: 0 for symbol only, 1+ to include children
- `substring_matching`: true for partial name matches
- `include_kinds`/`exclude_kinds`: Filter by LSP symbol kinds

**Name Path Patterns:**
- `"method"` - Matches any symbol named "method" anywhere
- `"Class/method"` - Matches "method" inside "Class" (relative path)
- `"/Class/method"` - Matches "method" inside top-level "Class" (absolute path)
- `"/Class"` - Matches only top-level "Class"

**Example:**
```
# Find all classes named "Main"
find_symbol(name_path="Main", include_body=false)

# Find specific method in specific file
find_symbol(
    name_path="BookingManager/saveBookings",
    relative_path="src/business/BookingManager.java",
    include_body=true
)

# Find class with its methods (depth=1)
find_symbol(
    name_path="Inputter",
    relative_path="src/util/Inputter.java",
    include_body=false,
    depth=1
)

# Find all methods (kind=6)
find_symbol(
    name_path="get",
    substring_matching=true,
    include_kinds=[6]
)
```

**LSP Symbol Kinds Reference:**
- 1=File, 2=Module, 3=Namespace, 4=Package
- **5=Class**, **6=Method**, 7=Property, 8=Field
- 9=Constructor, 10=Enum, 11=Interface
- **12=Function**, 13=Variable, 14=Constant

##### `find_referencing_symbols`
**Purpose:** Find all places where a symbol is used

**When to use:**
- Understanding symbol dependencies
- Finding all usages before refactoring
- Impact analysis for changes
- **Use before editing a symbol to ensure backward compatibility**

**Parameters:**
- `name_path`: Symbol to find references for
- `relative_path`: File containing the symbol (required, must be a file)

**Example:**
```
find_referencing_symbols(
    name_path="BookingManager/cancelBooking",
    relative_path="src/business/BookingManager.java"
)
```

##### `search_for_pattern`
**Purpose:** Flexible regex-based content search

**When to use:**
- Don't know exact symbol name
- Searching for patterns across files
- Need to search non-code files (HTML, config, etc.)
- Finding string literals or comments
- When symbolic search doesn't work

**Parameters:**
- `substring_pattern`: Regex pattern
- `relative_path`: File or directory (optional)
- `restrict_search_to_code_files`: true for only code, false for all files
- `paths_include_glob`/`paths_exclude_glob`: File filtering
- `context_lines_before`/`context_lines_after`: Context around matches
- `multiline`: true for patterns spanning multiple lines

**Example:**
```
# Find all TODO comments
search_for_pattern(
    substring_pattern="// TODO:.*",
    restrict_search_to_code_files=true
)

# Find package declarations
search_for_pattern(
    substring_pattern="package\\s+\\w+;",
    relative_path="src",
    context_lines_after=2
)

# Find multi-line patterns
search_for_pattern(
    substring_pattern="class.*?\\{",
    multiline=true,
    restrict_search_to_code_files=true
)
```

---

#### 4. Code Editing Tools

##### `replace_symbol_body`
**Purpose:** Replace entire symbol body

**When to use:**
- Rewriting a complete method/function
- Changing entire class implementation
- **Only use when you know the exact symbol body**
- After retrieving symbol with `find_symbol` first

**Parameters:**
- `name_path`: Symbol to replace
- `relative_path`: File containing symbol
- `body`: New symbol body (including signature for methods)

**Example:**
```
# First, find the symbol to see current body
find_symbol(
    name_path="BookingManager/saveBookings",
    relative_path="src/business/BookingManager.java",
    include_body=true
)

# Then replace it
replace_symbol_body(
    name_path="BookingManager/saveBookings",
    relative_path="src/business/BookingManager.java",
    body="""public boolean saveBookings() {
    boolean success = FileHandler.writeBinaryFile(BOOKING_FILE, bookings);
    if (success) {
        dataChanged = false;
        System.out.println("Bookings saved successfully!");
    }
    return success;
}"""
)
```

**Important Notes:**
- Body includes method signature and implementation
- Body does NOT include Javadoc comments or imports
- Must preserve exact indentation

##### `insert_after_symbol`
**Purpose:** Insert content after a symbol

**When to use:**
- Adding new method after existing method
- Adding new class after existing class
- Adding field after last field
- **Common use:** Add to end of file by inserting after last symbol

**Parameters:**
- `name_path`: Symbol to insert after
- `relative_path`: File containing symbol
- `body`: Content to insert

**Example:**
```
# Add new method after existing method
insert_after_symbol(
    name_path="BookingManager/saveBookings",
    relative_path="src/business/BookingManager.java",
    body="""
    /**
     * Delete all bookings.
     */
    public void deleteAllBookings() {
        bookings.clear();
        dataChanged = true;
    }
"""
)
```

##### `insert_before_symbol`
**Purpose:** Insert content before a symbol

**When to use:**
- Adding import before first class
- Adding new method before specific method
- Adding field before first field
- Adding class before existing class

**Parameters:**
- `name_path`: Symbol to insert before
- `relative_path`: File containing symbol
- `body`: Content to insert

**Example:**
```
# Add import before first class
insert_before_symbol(
    name_path="/BookingManager",  # Absolute path for top-level symbol
    relative_path="src/business/BookingManager.java",
    body="import java.util.stream.Collectors;\n"
)
```

---

#### 5. Reflection Tools

##### `think_about_collected_information`
**Purpose:** Reflect on whether you have enough information

**When to use:**
- **ALWAYS call after multiple search/read operations**
- After using find_symbol, search_for_pattern, etc.
- Before making code changes
- To verify you understand the codebase

**What it does:**
- Prompts you to assess collected information
- Identify missing information
- Determine next steps

##### `think_about_task_adherence`
**Purpose:** Verify you're still on track with the task

**When to use:**
- **ALWAYS call before insert/replace/delete operations**
- Long conversations with lots of back-and-forth
- Before making significant changes
- When task seems complex

##### `think_about_whether_you_are_done`
**Purpose:** Assess if task is complete

**When to use:**
- **ALWAYS call when you think you're done**
- Before reporting completion to user
- After implementing all requirements

---

### Best Practices

#### Efficient Code Reading Workflow

**1. Start with Directory Structure**
```
list_dir(relative_path=".", recursive=false)
list_dir(relative_path="src", recursive=true)
```

**2. Find Relevant Files**
```
find_file(file_mask="Main.java", relative_path="src")
find_file(file_mask="*Manager.java", relative_path="src/business")
```

**3. Get Symbol Overview (NOT full file)**
```
get_symbols_overview(relative_path="src/business/BookingManager.java")
```

**4. Find Specific Symbols**
```
find_symbol(
    name_path="BookingManager",
    relative_path="src/business/BookingManager.java",
    include_body=false,
    depth=1  # Get methods list
)
```

**5. Read Only What You Need**
```
find_symbol(
    name_path="BookingManager/saveBookings",
    relative_path="src/business/BookingManager.java",
    include_body=true  # Now read specific method
)
```

**6. Reflect**
```
think_about_collected_information()
```

#### Efficient Code Editing Workflow

**1. Find Symbol First**
```
find_symbol(
    name_path="BookingManager/cancelBooking",
    relative_path="src/business/BookingManager.java",
    include_body=true
)
```

**2. Check References**
```
find_referencing_symbols(
    name_path="BookingManager/cancelBooking",
    relative_path="src/business/BookingManager.java"
)
```

**3. Think Before Editing**
```
think_about_task_adherence()
```

**4. Make the Edit**
```
replace_symbol_body(...)
# or
insert_after_symbol(...)
```

#### Common Mistakes to Avoid

❌ **DON'T:**
- Read entire files when you only need one method
- Use search_for_pattern when find_symbol would work
- Read the same content multiple times with different tools
- Edit symbols without checking references first
- Forget to call reflection tools

✅ **DO:**
- Start with get_symbols_overview
- Use find_symbol for targeted reading
- Use search_for_pattern only when necessary
- Check references before editing
- Call reflection tools regularly

#### Performance Tips

1. **Use `relative_path` parameter** to narrow search scope
2. **Set `include_body=false`** when you only need metadata
3. **Use `depth` parameter** to get children without full bodies
4. **Leverage symbol kinds filtering** to reduce results
5. **Trust the cache** - repeated queries are fast

---

### Quick Reference

**Exploring new codebase:**
```
1. list_dir(relative_path=".", recursive=true)
2. find_file(file_mask="*.java", relative_path="src")
3. get_symbols_overview(relative_path="src/controller/Main.java")
4. find_symbol(name_path="Main", include_body=false, depth=1)
```

**Finding and editing a method:**
```
1. find_symbol(name_path="Class/method", include_body=true)
2. find_referencing_symbols(name_path="Class/method", relative_path="...")
3. think_about_task_adherence()
4. replace_symbol_body(name_path="Class/method", body="...")
```

**Searching for unknown code:**
```
1. search_for_pattern(substring_pattern="keyword", relative_path="src")
2. find_symbol(name_path="...", include_body=true)
3. think_about_collected_information()
```

**Adding new code:**
```
1. get_symbols_overview(relative_path="target_file.java")
2. insert_after_symbol(name_path="LastMethod", body="...")
# or
3. insert_before_symbol(name_path="FirstClass", body="import ...")
```