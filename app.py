import os
from google import genai
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

# Use environment variable for API key instead of hardcoding
api_key = "AIzaSyD6OVR_dU_RIv2U-5Wy7dulQEX4M_h7fzE"
if not api_key:
    raise ValueError("Please set GOOGLE_GENAI_API_KEY environment variable")

client = genai.Client(api_key=api_key)

class Issue(BaseModel):  # Fixed typo: "Issuse" -> "Issue"
    line_number: int
    severity: str
    category: str
    message: str
    suggestion: str
    code_snippet: Optional[str] = None  # Use Optional for better compatibility

def display_analysis_results(issues_json: str, file_path: str):
    """
    Parse and display the analysis results with line validation.
    """
    try:
        import json
        
        # Parse the JSON response
        if isinstance(issues_json, str):
            issues = json.loads(issues_json)
        else:
            issues = issues_json
        
        if not issues:
            print("✅ No issues found in the code!")
            return
        
        # Read the original file to validate line numbers
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        print(f"\n🔍 Found {len(issues)} issue(s) in {file_path}")
        print("=" * 80)
        
        for i, issue in enumerate(issues, 1):
            severity_emoji = {
                'Critical': '🚨',
                'High': '⚠️',
                'Medium': '⚡',
                'Low': '💡'
            }.get(issue.get('severity', 'Medium'), '📝')
            
            line_num = issue.get('line_number', 0)
            
            print(f"\n{severity_emoji} Issue #{i} - {issue.get('severity', 'Unknown')} Severity")
            print(f"📍 Line: {line_num}")
            
            # Validate line number
            if line_num > total_lines or line_num < 1:
                print(f"   ⚠️  WARNING: Line number {line_num} is out of range (file has {total_lines} lines)")
            else:
                # Show the actual line content
                actual_line = lines[line_num - 1].strip()
                print(f"   Code: {actual_line}")
            
            print(f"🏷️  Category: {issue.get('category', 'Unknown')}")
            print(f"📝 Message: {issue.get('message', 'No message')}")
            print(f"💡 Suggestion: {issue.get('suggestion', 'No suggestion')}")
            
            if issue.get('code_snippet'):
                print(f"📋 Code Snippet: {issue.get('code_snippet')}")
            
            print("-" * 80)
            
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing analysis results: {e}")
        print("Raw response:")
        print(issues_json)
    except Exception as e:
        print(f"❌ Error displaying results: {e}")
def analyze_code_file(file_path: str, mime_type: str = "text/plain") -> str:
    try:
        # Verify file exists before uploading
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Try uploading with path and mime_type
        try:
            uploaded_file = client.files.upload(path=file_path, mime_type=mime_type)
        except TypeError:
            # Fallback: try with just path parameter
            try:
                uploaded_file = client.files.upload(path=file_path)
            except TypeError:
                # Read file with line numbers for better accuracy
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Create numbered content
                numbered_content = ""
                for i, line in enumerate(lines, 1):
                    numbered_content += f"{i:4d}: {line}"
                
                # Generate analysis with numbered content
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=[
                        f"""You are an expert programmer and software tester who analyzes code for bugs — from minor syntax errors to major security vulnerabilities.
                        
                        IMPORTANT: The code below is provided with line numbers (format: "LINE_NUMBER: code"). When reporting issues, use the EXACT line number shown in the format "LINE_NUMBER:" at the beginning of each line.
                        
                        Task:
                        Analyze the following {Path(file_path).suffix} code for issues in the following categories:
                        - Syntax errors and language-specific issues
                        - Security vulnerabilities (SQL injection, XSS, CSRF, etc.)
                        - Performance bottlenecks
                        - Logic errors and potential bugs
                        - Code readability and maintainability
                        - Best practices violations
                        
                        For PHP files specifically:
                        - Ensure proper semicolon usage
                        - Check for proper error handling
                        - Validate input sanitization
                        - Review database query security
                        - Check for proper PHP opening/closing tags
                        
                        Provide detailed, actionable feedback for each issue found.
                        Rate severity as: Critical, High, Medium, Low
                        
                        For each issue:
                        - Use the EXACT line number from the numbered code below
                        - Include the problematic code snippet from that line
                        - Provide specific suggestions for fixing the issue
                        
                        Code to analyze (with line numbers):
                        ```{Path(file_path).suffix[1:]}
                        {numbered_content}
                        ```
                        """
                    ],
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": list[Issue],
                    },
                )
                
                return response.text
        
        # Generate analysis
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",  # Updated to latest model
            contents=[
                """You are an expert programmer and software tester who analyzes code for bugs — from minor syntax errors to major security vulnerabilities.
                
                Task:
                Analyze the uploaded code file for issues in the following categories:
                - Syntax errors and language-specific issues
                - Security vulnerabilities (SQL injection, XSS, CSRF, etc.)
                - Performance bottlenecks
                - Logic errors and potential bugs
                - Code readability and maintainability
                - Best practices violations
                
                For PHP files specifically:
                - Ensure proper semicolon usage
                - Check for proper error handling
                - Validate input sanitization
                - Review database query security
                
                Provide detailed, actionable feedback for each issue found.
                Rate severity as: Critical, High, Medium, Low
                """, 
                uploaded_file
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema": list[Issue],
            },
        )
        
        return response.text
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return []

# Main execution
if __name__ == "__main__":
    file_to_analyze = "editPage.php"  # Make this configurable
    
    # Determine MIME type based on file extension
    file_extension = Path(file_to_analyze).suffix.lower()
    mime_type_map = {
        '.php': 'application/x-httpd-php',
        '.py': 'text/x-python',
        '.js': 'application/javascript',
        '.html': 'text/html',
        '.css': 'text/css',
        '.sql': 'application/sql',
        '.java': 'text/x-java-source',
        '.cpp': 'text/x-c++src',
        '.c': 'text/x-csrc',
    }
    
    mime_type = mime_type_map.get(file_extension, 'text/plain')
    
    
    print(f"Analyzing {file_to_analyze} (MIME type: {mime_type})...")
    issues = analyze_code_file(file_to_analyze, mime_type)
    
    if issues:
        display_analysis_results(issues, file_to_analyze)
    else:
        print("No issues found or analysis failed.")
    file_to_analyze = "editPage.php"  # Make this configurable
    
    # Determine MIME type based on file extension
    file_extension = Path(file_to_analyze).suffix.lower()
    mime_type_map = {
        '.php': 'application/x-httpd-php',
        '.py': 'text/x-python',
        '.js': 'application/javascript',
        '.html': 'text/html',
        '.css': 'text/css',
        '.sql': 'application/sql',
        '.java': 'text/x-java-source',
        '.cpp': 'text/x-c++src',
        '.c': 'text/x-csrc',
    }
    
    mime_type = mime_type_map.get(file_extension, 'text/plain')
    
    print(f"Analyzing {file_to_analyze} (MIME type: {mime_type})...")
    issues = analyze_code_file(file_to_analyze, mime_type)
    
    if issues:
        print("\n=== CODE ANALYSIS RESULTS ===")
        print(issues)
    else:
        print("No issues found or analysis failed.")
    file_to_analyze = "editPage.php"  # Make this configurable
    
    # Determine MIME type based on file extension
    file_extension = Path(file_to_analyze).suffix.lower()
    mime_type_map = {
        '.php': 'application/x-httpd-php',
        '.py': 'text/x-python',
        '.js': 'application/javascript',
        '.html': 'text/html',
        '.css': 'text/css',
        '.sql': 'application/sql',
        '.java': 'text/x-java-source',
        '.cpp': 'text/x-c++src',
        '.c': 'text/x-csrc',
    }
    
    mime_type = mime_type_map.get(file_extension, 'text/plain')
    
    print(f"Analyzing {file_to_analyze} (MIME type: {mime_type})...")
    issues = analyze_code_file(file_to_analyze, mime_type)
    
    if issues:
        print("\n=== CODE ANALYSIS RESULTS ===")
        print(issues)
    else:
        print("No issues found or analysis failed.")