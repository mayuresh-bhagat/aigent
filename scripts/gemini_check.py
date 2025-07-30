import os
import requests

GEMINI_API_KEY = "AIzaSyD6OVR_dU_RIv2U-5Wy7dulQEX4M_h7fzE"

def get_changed_files():
    from subprocess import check_output
    return check_output(["git", "diff", "--name-only", "origin/dev...HEAD"]).decode().splitlines()

def call_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(f"{url}?key={GEMINI_API_KEY}", json=payload, headers=headers)
    return response.json()['candidates'][0]['content']['parts'][0]['text']

def main():
    files = get_changed_files()
    output = []
    for file in files:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            prompt = f"Review this code for vulnerabilities, bad practices, and outdated syntax:\n\n{content}"
            result = call_gemini(prompt)
            output.append(f"### {file}\n{result}\n")
    with open("gemini_report.md", "w") as out:
        out.writelines(output)

if __name__ == "__main__":
    main()
