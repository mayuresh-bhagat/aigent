import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List
import google.generativeai as genai

# --- Pydantic Models ---
class Issue(BaseModel):
    line_number: int
    severity: str
    category: str
    message: str
    suggestion: str
    code_snippet: Optional[str] = None

# --- Gemini API Configuration ---
def configure_gemini_api():
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Environment variable GOOGLE_GEMINI_API_KEY not set. Please add it to your GitHub Secrets.")
    genai.configure(api_key=api_key)

# --- Code Analysis Function ---
def analyze_code_content(file_path: str, file_content: str, mime_type: str) -> List[Issue]:
    try:
        model = genai.GenerativeModel("gemini-pro")

        lines = file_content.splitlines()
        numbered_content = "\n".join(f"{i:4d}: {line}" for i, line in enumerate(lines, 1))

        prompt = f"""You are an expert programmer and software tester who analyzes code for bugs.

IMPORTANT: The code below includes line numbers in the format "LINE_NUMBER: code".

Analyze this {Path(file_path).suffix[1:] or 'text'} code for:
- Syntax Errors
- Security Vulnerabilities
- Performance Bottlenecks
- Logic Errors
- Code Readability & Maintainability
- Best Practices Violations

For PHP files, also check:
- Semicolon usage
- Error handling
- Input sanitization
- Parameterized queries
- Correct PHP tags

Respond ONLY with a valid JSON array of objects having:
- line_number (int)
- severity ("Critical"|"High"|"Medium"|"Low")
- category
- message
- suggestion
- code_snippet (optional)

Return [] if no issues.

Code to analyze:

{numbered_content}
"""

        response = model.generate_content(prompt)
        text = response.candidates[0].content.parts[0].text.strip()

        # Parse and validate JSON
        issues_data = json.loads(text)
        return [Issue(**issue) for issue in issues_data]

    except Exception as e:
        print(f"Error during analysis of {file_path}: {e}")
        return []

# --- Display Results Function ---
def display_analysis_results(issues: List[Issue], file_path: str):
    if not issues:
        print(f"✅ No issues found in {file_path}")
        return

    print(f"\n🔍 Found {len(issues)} issue(s) in {file_path}")
    print("=" * 80)

    for i, issue in enumerate(issues, 1):
        severity_emoji = {
            'Critical': '🚨',
            'High': '⚠️',
            'Medium': '⚡',
            'Low': '💡'
        }.get(issue.severity, '📝')

        annotation_level = {
            'Critical': 'error',
            'High': 'error',
            'Medium': 'warning',
            'Low': 'notice'
        }.get(issue.severity, 'notice')

        print(f"\n{severity_emoji} Issue #{i} - {issue.severity} Severity")
        print(f"📍 Line: {issue.line_number}")
        print(f"🏷️ Category: {issue.category}")
        print(f"📝 Message: {issue.message}")
        if issue.code_snippet:
            print(f"📋 Code Snippet: `{issue.code_snippet.strip()}`")
        print(f"💡 Suggestion: {issue.suggestion}")
        print("-" * 80)

        annotation = (
            f"::{annotation_level} file={file_path},line={issue.line_number}::"
            f"{issue.category} ({issue.severity}): {issue.message}. Suggestion: {issue.suggestion}"
        )
        print(annotation)

# --- Main Execution ---
if __name__ == "__main__":
    configure_gemini_api()

    changed_files_json = os.getenv("CHANGED_FILES")
    if not changed_files_json:
        print("Environment variable 'CHANGED_FILES' not set or empty.")
        exit(0)

    try:
        changed_files = [f for f in json.loads(changed_files_json) if f]
    except json.JSONDecodeError:
        print(f"Error parsing CHANGED_FILES: {changed_files_json}")
        exit(1)

    if not changed_files:
        print("No changed files found.")
        exit(0)

    has_issues = False
    for file_path in changed_files:
        if not Path(file_path).is_file():
            print(f"Skipping {file_path}: Not found or deleted.")
            continue

        ext = Path(file_path).suffix.lower()
        mime_type = {
            '.php': 'application/x-httpd-php',
            '.py': 'text/x-python',
            '.js': 'application/javascript',
            '.html': 'text/html',
            '.css': 'text/css',
            '.sql': 'application/sql',
            '.java': 'text/x-java-source',
            '.cpp': 'text/x-c++src',
            '.c': 'text/x-csrc',
            '.ts': 'application/typescript',
            '.go': 'text/x-go',
            '.rb': 'application/x-ruby',
            '.xml': 'application/xml',
            '.json': 'application/json',
            '.yml': 'text/yaml',
            '.yaml': 'text/yaml',
        }.get(ext, 'text/plain')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"ERROR: Cannot read {file_path}: {e}")
            continue

        print(f"\n--- Analyzing {file_path} ({mime_type}) ---")
        issues = analyze_code_content(file_path, content, mime_type)

        if issues:
            has_issues = True
        display_analysis_results(issues, file_path)

    if has_issues:
        print("\n🚨 Issues found. Please fix them before merging.")
        exit(1)
    else:
        print("\n✅ All clear. No critical issues found.")
        exit(0)
