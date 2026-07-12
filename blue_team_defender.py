
import sys, os
# Force the agent to use your venv libraries
sys.path.insert(0, r'C:\Users\tebibu\.gemini\antigravity\scratch\agent_company\venv\Lib\site-packages')

import re, ollama, argparse

AGENT_NAME = "Blue Team Defender"
SYSTEM_PROMPT = "You are a professional Blue Team Defender. Act as an expert in this field and provide clean, modular code."

base_dir = r'C:\Users\tebibu\.gemini\antigravity\scratch\agent_company'
work_dir = os.path.join(base_dir, f"work_{AGENT_NAME.lower().replace(' ', '_')}")
os.makedirs(work_dir, exist_ok=True)

def read_shared_memory(target_agent):
    path = os.path.join(base_dir, f"work_{target_agent.lower().replace(' ', '_')}")
    if os.path.exists(path):
        content = ""
        for f in os.listdir(path):
            if f.endswith('.py'):
                with open(os.path.join(path, f), 'r', encoding='utf-8') as file:
                    content += f"\n--- {f} ---\n{file.read()}\n"
        return content
    return ""

def run_agent(goal):
    context = ""
    # Example logic to pull from other agents
    if "tech_lead" in goal.lower(): context += read_shared_memory("tech_lead")
    
    prompt = f"{SYSTEM_PROMPT}\nContext: {context}\nGoal: {goal}.\nFormat: [FILENAME: filename.py] followed by code."
    response = ollama.chat(model='qwen2.5-coder:7b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

parser = argparse.ArgumentParser()
parser.add_argument('--task', required=True)
args = parser.parse_args()

content = run_agent(args.task)
files = re.findall(r"\[FILENAME: (.*?)\](.*?)(?=\[FILENAME: |$)", content, re.DOTALL)

if files:
    for name, code in files:
        with open(os.path.join(work_dir, name.strip()), "w", encoding="utf-8") as f:
            f.write(code.strip())
    print(f"{AGENT_NAME} success: created {len(files)} files.")
else:
    with open(os.path.join(work_dir, "output.txt"), "w", encoding="utf-8") as f:
        f.write(content)
