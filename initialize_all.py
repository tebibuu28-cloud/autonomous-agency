import os

agents = [
    # ... (Keep your 65 agent names here)
]

template_code = """
import sys, os
sys.path.insert(0, r'C:\\Users\\tebibu\\.gemini\\antigravity\\scratch\\agent_company\\venv\\Lib\\site-packages')
import re, ollama, argparse

AGENT_NAME = "{name}"
SKILLS_DIR = r'C:\\Users\\tebibu\\.gemini\\antigravity\\scratch\\agent_company\\skills'

def get_expert_context():
    # Agent automatically references local GitHub repo code for context
    context = ""
    for category in os.listdir(SKILLS_DIR):
        if category in AGENT_NAME.lower():
            path = os.path.join(SKILLS_DIR, category)
            # Read first few relevant files as reference
            for f in os.listdir(path)[:3]:
                if f.endswith('.py'):
                    with open(os.path.join(path, f), 'r', encoding='utf-8', errors='ignore') as file:
                        context += f"\\n--- Expert Pattern: {{f}} ---\\n{{file.read()[:500]}}\\n"
    return context

def run_agent(goal):
    context = get_expert_context()
    prompt = f"{{AGENT_NAME}} Expert Context:\\n{{context}}\\n\\nGoal: {{goal}}.\\nFormat: [FILENAME: filename.py] followed by code."
    response = ollama.chat(model='qwen2.5-coder:7b', messages=[{{'role': 'user', 'content': prompt}}])
    return response['message']['content']

# ... (rest of your existing dispatcher logic)
"""

for agent in agents:
    with open(f"{agent}.py", "w", encoding="utf-8") as f:
        f.write(template_code.format(name=agent.replace('_', ' ').title()))