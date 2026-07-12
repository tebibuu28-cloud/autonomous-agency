import sys
import os
import re

# Standardized Pathing
base_dir = r'C:\Users\tebibu\.gemini\antigravity\scratch\agent_company'
sys.path.insert(0, os.path.join(base_dir, 'venv', 'Lib', 'site-packages'))

import ollama
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--department', required=True)
parser.add_argument('--agent', required=True)
parser.add_argument('--task', required=True)
args, unknown = parser.parse_known_args()

work_dir = os.path.join(base_dir, f"work_{args.agent.lower().replace(' ', '_')}")
os.makedirs(work_dir, exist_ok=True)

def read_shared_memory(target_agent_name):
    path = os.path.join(base_dir, f"work_{target_agent_name.lower().replace(' ', '_')}")
    if os.path.exists(path):
        context = ""
        for f in os.listdir(path):
            if f.endswith('.py'):
                with open(os.path.join(path, f), 'r', encoding='utf-8') as file:
                    context += f"\n--- {f} ---\n{file.read()}\n"
        return context
    return "No prior work found."

def perform_task(goal):
    # Auto-detection of dependencies
    context = ""
    if "data_engineer" in goal.lower(): context += read_shared_memory("data_engineer")
    if "quantitative_analyst" in goal.lower(): context += read_shared_memory("quantitative_analyst")
    
    prompt = (f"You are a professional {args.agent}. Context from team: {context}\n\n"
              f"Goal: {goal}. Format: [FILENAME: filename.py] followed by code. No backticks.")
    
    response = ollama.chat(model='qwen2.5-coder:7b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

content = perform_task(args.task)
files = re.findall(r"\[FILENAME: (.*?)\](.*?)(?=\[FILENAME: |$)", content, re.DOTALL)

if files:
    for name, code in files:
        with open(os.path.join(work_dir, name.strip()), "w", encoding="utf-8") as f:
            f.write(code.strip())
    print(f"Agent successfully built {len(files)} files in {work_dir}")
else:
    with open(os.path.join(work_dir, "output.txt"), "w", encoding="utf-8") as f:
        f.write(content)