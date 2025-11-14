# GitHub Copilot Agent System - Setup Guide

## Overview
This system provides 7 specialized agents for Python data science development in VSCode with GitHub Copilot. Each agent has a specific role and follows consistent standards defined in `Instructions.md`.

## Agent Roster

| Agent | Primary Focus | Key Strength |
|-------|--------------|--------------|
| **Architect** | System design, OOP, SOLID principles | Ensures clean architecture and proper abstractions |
| **Developer** | Implementation, type safety, readability | Writes production-quality, maintainable code |
| **Analyst** | Data exploration, initial profiling | Discovers insights and data quality issues |
| **Code Reviewer** | Standards enforcement, refactoring | Maintains code quality and tracks improvements |
| **Tester** | Unit testing with pytest | Ensures reliability and testability |
| **Logging Master** | Structured logging, no print statements | Makes debugging efficient and professional |
| **Debugger** | Troubleshooting, root cause analysis | Solves problems methodically |

## Setup Instructions

### 1. Add Instructions.md to Your Project
```bash
# In your project root
touch Instructions.md
# Copy the content from the "Instructions.md - Global Code Standards" artifact
```

This file serves as the foundation that all agents reference.

### 2. Configure GitHub Copilot Custom Instructions

In VSCode:
1. Open Command Palette (`Cmd/Ctrl + Shift + P`)
2. Search for "GitHub Copilot: Edit Custom Instructions"
3. Create a new mode for each agent
4. Copy the corresponding agent instructions

### 3. Create Project Structure
```bash
# Standard structure
mkdir -p data/{raw,processed,external}
mkdir -p notebooks/{exploratory,final}
mkdir -p src/{config,data,models,utils}
mkdir -p tests/{test_data,test_models}
mkdir -p scripts

# Create essential files
touch src/__init__.py
touch src/config/__init__.py
touch src/config/logging_config.py  # Copy logging setup from Instructions.md
touch IMPROVEMENTS.md
touch README.md
```

### 4. Initialize with uv
```bash
# If using uv for dependency management
uv init your_project_name
cd your_project_name

# Add common data science dependencies
uv add pandas numpy scikit-learn matplotlib seaborn
uv add jupyter ipykernel  # For notebooks
uv add pytest pytest-cov  # For testing
uv add ruff  # For formatting

# Optional profiling tools for Analyst
uv add ydata-profiling sweetviz
```

### 5. Configure Ruff
```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "C4", "PT"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## Using the Agents

### Typical Workflow

#### 1. Starting a New Project
**Use: Architect Agent**
```
"As the Architect, help me set up a project for [description]. 
What structure and main classes should I create?"
```

#### 2. Exploring New Data
**Use: Analyst Agent**
```
"As the Analyst, create an exploratory notebook for this dataset. 
File: data/raw/dataset.csv"
```

#### 3. Implementing Features
**Use: Developer Agent**
```
"As the Developer, implement a data preprocessing pipeline 
with proper type hints and logging."
```

#### 4. Writing Tests
**Use: Tester Agent**
```
"As the Tester, create unit tests for the preprocessing module."
```

#### 5. Reviewing Code
**Use: Code Reviewer Agent**
```
"As the Code Reviewer, review src/data/preprocessing.py 
and update IMPROVEMENTS.md with any issues."
```

#### 6. Fixing Logging Issues
**Use: Logging Master Agent**
```
"As the Logging Master, review this module and replace 
print statements with proper logging."
```

#### 7. Debugging
**Use: Debugger Agent**
```
"As the Debugger, help me fix this error: [paste error].
Here's the relevant code: [paste code]"
```

### Agent Combinations

**Major Feature Development**:
1. **Architect**: Design the components and interfaces
2. **Developer**: Implement the solution
3. **Logging Master**: Review logging practices
4. **Tester**: Write tests
5. **Code Reviewer**: Final review and IMPROVEMENTS.md update

**Bug Investigation**:
1. **Debugger**: Identify root cause
2. **Developer**: Implement fix
3. **Tester**: Add regression test
4. **Code Reviewer**: Review and track if systematic issue

**Data Analysis Project**:
1. **Analyst**: Initial exploration and profiling
2. **Developer**: Convert insights to production code
3. **Architect**: Organize into proper modules
4. **Tester**: Test data processing logic

## IMPROVEMENTS.md Workflow

The `IMPROVEMENTS.md` file is central to maintaining code quality:

### When to Add Items
- **Code Reviewer**: Primary owner, adds most items
- **Tester**: Adds testing gaps and untestable code
- **Logging Master**: Adds widespread logging issues
- **Debugger**: Adds systematic problems discovered during debugging
- **Any Agent**: Can add items when they spot problems

### File Format
```markdown
# Technical Debt & Improvement Tracking

**Last Updated**: YYYY-MM-DD

## 🔴 High Priority
[Critical issues that need immediate attention]

## 🟡 Medium Priority
[Important improvements that can wait]

## 🟢 Low Priority
[Nice-to-haves and optimizations]

## ✅ Completed
[Fixed issues with resolution details]
```

### Review Regularly
- Weekly review with Code Reviewer
- Address high priority items promptly
- Move completed items to bottom with details

## Best Practices

### Switching Between Agents
**In VSCode with Copilot**:
- Use the custom instruction mode selector
- Clearly state which agent you want: "As the Architect..."
- Each agent will respect the global Instructions.md

### Asking Good Questions

**❌ Vague**:
```
"Fix this code"
"Make this better"
"Write some tests"
```

**✅ Specific**:
```
"As the Developer, refactor this function to follow SRP 
and add type hints"

"As the Code Reviewer, identify SOLID principle violations 
in this class"

"As the Tester, write unit tests for edge cases in 
the normalize_data function"
```

### Maintaining Consistency

1. **Always reference Instructions.md**
   - All agents follow these standards
   - Update Instructions.md if standards change
   - Don't ask agents to violate standards

2. **Keep IMPROVEMENTS.md updated**
   - Review regularly
   - Mark items as completed
   - Use priority levels

3. **Use global logger everywhere**
   - Import from `src.config.logging_config`
   - Never use print() for logging
   - Logging Master enforces this

4. **Write tests as you go**
   - Don't defer all testing to end
   - Test after implementing features
   - Tester helps maintain coverage

## Common Patterns

### Pattern 1: New Feature Development
```bash
# 1. Design (Architect)
"As the Architect, design a model training pipeline"

# 2. Implement (Developer)
"As the Developer, implement the ModelTrainer class 
with type hints and logging"

# 3. Test (Tester)
"As the Tester, create tests for ModelTrainer"

# 4. Review (Code Reviewer)
"As the Code Reviewer, review the training pipeline 
and update IMPROVEMENTS.md"
```

### Pattern 2: Code Cleanup
```bash
# 1. Identify (Code Reviewer)
"As the Code Reviewer, review src/data/ for 
code quality issues"

# 2. Fix (Developer)
"As the Developer, refactor the DataProcessor class 
based on reviewer feedback"

# 3. Verify (Tester)
"As the Tester, ensure tests still pass after refactoring"
```

### Pattern 3: Bug Fix
```bash
# 1. Diagnose (Debugger)
"As the Debugger, help me understand this error: [error]"

# 2. Fix (Developer)
"As the Developer, implement the fix suggested by Debugger"

# 3. Prevent (Tester)
"As the Tester, add a test to catch this bug in the future"

# 4. Review (Code Reviewer)
"As the Code Reviewer, check if this is a systemic issue"
```

## Tips for Success

### 1. Be Specific About Context
```
"As the Developer, I'm working on a time series forecasting 
project using DARTS. Implement a function to prepare 
sequences for LSTM training."
```

### 2. Reference Existing Code
```
"As the Code Reviewer, review this code from 
src/models/train.py lines 45-80. Check for SOLID violations."
```

### 3. Ask for Explanations
```
"As the Architect, explain why dependency injection is 
better than direct instantiation in this case."
```

### 4. Request Examples
```
"As the Tester, show me how to test a function that uses 
pandas DataFrames with pytest fixtures."
```

### 5. Combine Agents When Needed
```
"As the Code Reviewer and Logging Master together, 
review this module for both code quality and logging issues."
```

## Troubleshooting

### Agent Not Following Standards?
- Explicitly reference Instructions.md in your prompt
- Quote specific sections: "Instructions.md says type hints are non-negotiable"
- Be more directive: "Follow the Numpy docstring format from Instructions.md"

### Inconsistent Responses?
- Start conversations with agent role: "As the [Agent]..."
- Include context: "This is for [project type], using [libraries]"
- Reference Instructions.md early in conversation

### Need Different Behavior?
- Update Instructions.md, not individual agents
- Individual agents follow Instructions.md as foundation
- Agent-specific instructions are in addition to, not replacement of, Instructions.md

## Extending the System

### Adding New Agents
If you need additional specialized agents:

1. Create role definition
2. Define specific responsibilities
3. Ensure it references Instructions.md
4. Add to this guide
5. Specify how it works with existing agents

### Modifying Standards
To change project standards:

1. Update Instructions.md first
2. All agents will follow new standards
3. Update existing code to match
4. Consider backward compatibility

### Project-Specific Customization
For project-specific needs:

1. Keep Instructions.md general
2. Add project-specific details to individual agents
3. Use IMPROVEMENTS.md for project-specific debt tracking
4. Maintain consistency across agents

## Quick Reference

### Agent Selection Guide

**Need to...**
- Design system architecture → **Architect**
- Implement new feature → **Developer**
- Explore new dataset → **Analyst**
- Review code quality → **Code Reviewer**
- Write tests → **Tester**
- Fix logging issues → **Logging Master**
- Debug an error → **Debugger**

### File Locations

```
project/
├── Instructions.md              # Global standards (all agents)
├── IMPROVEMENTS.md              # Technical debt tracking
├── src/config/logging_config.py # Global logger setup
├── tests/                       # Unit tests
└── notebooks/                   # Exploratory work
```

### Key Commands

```bash
# Format code with ruff
ruff format .

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Install dependencies
uv add <package>

# Sync dependencies
uv sync
```

## Final Notes

This system is designed to be:
- **Consistent**: All agents follow Instructions.md
- **Collaborative**: Agents reference each other's work
- **Maintainable**: IMPROVEMENTS.md tracks technical debt
- **Professional**: Enterprise-grade code standards
- **Practical**: Focused on real data science workflows

Start with Instructions.md, pick the right agent for each task, and maintain IMPROVEMENTS.md. The agents will help you write better code that's easier to maintain, test, and debug.

Happy coding! 🚀