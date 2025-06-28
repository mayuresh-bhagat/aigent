# Python Setup Guide for Windows with Virtual Environment and Google GenAI

This guide will walk you through setting up Python on Windows, creating a virtual environment, and installing Google's Generative AI library.

## Prerequisites

- Windows 10 or later
- Administrator access (for Python installation)
- Internet connection

## Step 1: Install Python

### Option A: Download from Python.org (Recommended)

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.x version for Windows
3. Run the installer with the following important settings:
   - ✅ **Check "Add Python to PATH"** (very important!)
   - ✅ Check "Install launcher for all users"
   - Choose "Customize installation" for advanced options
   - ✅ Check "Add Python to environment variables"

### Option B: Using Microsoft Store

1. Open Microsoft Store
2. Search for "Python"
3. Install the latest Python version

### Verify Installation

Open Command Prompt or PowerShell and run:

```cmd
python --version
pip --version
```

You should see version numbers for both Python and pip.

## Step 2: Create a Virtual Environment

Virtual environments help isolate your project dependencies from other Python projects.

### Navigate to Your Project Directory

```cmd
# Create a new project folder
mkdir my-genai-project
cd my-genai-project
```

### Create Virtual Environment

```cmd
# Create virtual environment named 'venv'
python -m venv venv
```

### Activate Virtual Environment

**Command Prompt:**
```cmd
venv\Scripts\activate
```

**PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**Note:** If you get an execution policy error in PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Verify Virtual Environment

When activated, your prompt should show `(venv)` at the beginning:
```
(venv) C:\path\to\your\project>
```

## Step 3: Install Google GenAI Library

With your virtual environment activated, install the Google Generative AI library:

```cmd
pip install google-generativeai
```

## Step 4: Run Script

```cmd
python add.py
```

## Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Google AI Studio](https://makersuite.google.com/)
- [Google AI Python SDK Documentation](https://ai.google.dev/api/python)

---

**Happy coding! 🐍✨**