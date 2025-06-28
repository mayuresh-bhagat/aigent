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

### Install Additional Useful Packages

```cmd
# Install commonly used packages
pip install python-dotenv requests pillow
```

## Step 4: Set Up Google AI API Key

### Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

### Secure Your API Key

**Method 1: Using Environment Variables**

1. Create a `.env` file in your project root:
```
GOOGLE_API_KEY=your_api_key_here
```

2. Add `.env` to your `.gitignore` file to keep it private

**Method 2: System Environment Variable**

1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `GOOGLE_API_KEY`
6. Variable value: your API key

## Step 5: Create a Test Script

Create a file named `test_genai.py`:

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Create a model instance
model = genai.GenerativeModel('gemini-pro')

# Test the connection
try:
    response = model.generate_content("Hello! Can you tell me a fun fact about Python programming?")
    print("✅ Google GenAI setup successful!")
    print("Response:", response.text)
except Exception as e:
    print("❌ Error:", str(e))
```

### Run the Test

```cmd
python test_genai.py
```

## Step 6: Managing Your Environment

### Deactivate Virtual Environment

```cmd
deactivate
```

### Save Dependencies

Create a requirements file to share your project dependencies:

```cmd
pip freeze > requirements.txt
```

### Install from Requirements (for future setups)

```cmd
pip install -r requirements.txt
```

## Common Issues and Solutions

### Issue: 'python' is not recognized
**Solution:** Python is not added to PATH. Reinstall Python and check "Add Python to PATH".

### Issue: PowerShell execution policy error
**Solution:** Run PowerShell as administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: API key not found
**Solution:** 
- Verify your `.env` file is in the correct location
- Check that your API key is valid
- Restart your terminal after setting environment variables

### Issue: SSL certificate errors
**Solution:** 
```cmd
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org google-generativeai
```

## Project Structure

Your project should look like this:

```
my-genai-project/
│
├── venv/                 # Virtual environment (don't commit)
├── .env                  # Environment variables (don't commit)
├── .gitignore           # Git ignore file
├── requirements.txt     # Dependencies list
├── test_genai.py       # Your test script
└── README.md           # This file
```

## Next Steps

1. Explore the [Google AI Python SDK documentation](https://ai.google.dev/tutorials/python_quickstart)
2. Check out example projects and tutorials
3. Consider using Jupyter notebooks for experimentation:
   ```cmd
   pip install jupyter
   jupyter notebook
   ```

## Additional Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Google AI Studio](https://makersuite.google.com/)
- [Google AI Python SDK Documentation](https://ai.google.dev/api/python)

---

**Happy coding! 🐍✨**