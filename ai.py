#!/usr/bin/env python3
import sys
import requests
import json
import os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:1.5b"

def ask(prompt, files=None):
    context = ""
    if files:
        for f in files:
            try:
                with open(f, 'r') as fh:
                    context += f"\n--- FILE: {f} ---\n{fh.read()}\n"
            except FileNotFoundError:
                print(f"Error: {f} not found")
                sys.exit(1)
    
    full_prompt = context + "\n" + prompt if context else prompt
    
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": full_prompt,
        "stream": True
    })
    
    output = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            response_text = data.get("response", "")
            print(response_text, end="", flush=True)
            output += response_text
    print()
    
    # Save to timestamped file in home directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    home_dir = os.path.expanduser("~")
    output_file = os.path.join(home_dir, f"ai_output_{timestamp}.txt")
    
    with open(output_file, 'w') as f:
        f.write(f"Prompt:\n{prompt}\n\n")
        f.write(f"Files:\n{', '.join(files) if files else 'None'}\n\n")
        f.write(f"Output:\n{output}")
    
    print(f"\n[Saved to {output_file}]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ai.py 'your prompt' [file1] [file2] ...")
        sys.exit(1)
    
    prompt = sys.argv[1]
    files = sys.argv[2:] if len(sys.argv) > 2 else None
    ask(prompt, files)