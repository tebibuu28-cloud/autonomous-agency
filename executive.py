import sys
import os
import re

# Set path
sys.path.insert(0, r'C:\Users\tebibu\.gemini\antigravity\scratch\agent_company\venv\Lib\site-packages')

import ollama
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--department', required=True)
parser.add_argument('--agent', required=True)
parser.add_argument('--task', required=True)
args, unknown = parser.parse_known_args()

work_dir = f"work_{args.agent.lower().replace(' ', '_')}"
os.makedirs(work_dir, exist_ok=True)

def perform_task(goal):
    # This instruction forces the AI to use a simple, non-breaking format
    prompt = f"Goal: {goal}. Provide code files in this format: [FILENAME: filename.py] followed by the code. Do not use backticks."
    response = ollama.chat(model='qwen2.5-coder:7b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

content = perform_task(args.task)

# Self-contained parser that won't cause syntax errors
files = re.findall(r"\[FILENAME: (.*?)\](.*?)(?=\[FILENAME: |$)", content, re.DOTALL)

if files:
    for name, code in files:
        with open(os.path.join(work_dir, name.strip()), "w", encoding="utf-8") as f:
            f.write(code.strip())
    print(f"Agent successfully built files in {work_dir}")
else:
    with open(os.path.join(work_dir, "output.txt"), "w", encoding="utf-8") as f:
        f.write(content)