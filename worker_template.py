import os

agents = [
    # Technical Cluster
    "algorithmic_trader", "quantitative_analyst", "data_engineer", "tech_lead",
    "security_architect", "qa_automation", "cloud_architect", "blockchain_developer",
    "ai_ml_researcher", "db_administrator", "frontend_engineer", "backend_engineer",
    "devops_engineer", "product_designer", "ux_designer", "growth_hacker",
    "seo_specialist", "legal_compliance_ai", "business_analyst", "executive_assistant",
    # Operational/Strategic Cluster
    "brand_strategist", "cro_specialist", "social_media_manager", "copywriter", 
    "motion_designer", "ceo", "cfo", "coo", "market_researcher", 
    "business_dev_manager", "compliance_officer", "incident_responder", 
    "privacy_specialist", "penetration_tester", "qa_manager", 
    "hr_manager", "technical_writer", "release_manager", 
    "customer_support_lead", "infrastructure_manager"
]

for agent in agents:
    filename = f"{agent}.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f'''
import sys, os, re, ollama, argparse

AGENT_NAME = "{agent.replace('_', ' ').title()}"
SYSTEM_PROMPT = "You are an expert {agent.replace('_', ' ')}. Your decisions are data-driven and specialized in your domain."

base_dir = r'C:\\Users\\tebibu\\.gemini\\antigravity\\scratch\\agent_company'
work_dir = os.path.join(base_dir, f"work_{{AGENT_NAME.lower().replace(' ', '_')}}")
os.makedirs(work_dir, exist_ok=True)

def perform_task(goal):
    prompt = f"{{SYSTEM_PROMPT}}\\nGoal: {{goal}}.\\nFormat: [FILENAME: filename.py] followed by code. No backticks."
    response = ollama.chat(model='qwen2.5-coder:7b', messages=[{{'role': 'user', 'content': prompt}}])
    return response['message']['content']

parser = argparse.ArgumentParser()
parser.add_argument('--task', required=True)
args = parser.parse_args()

content = perform_task(args.task)
files = re.findall(r"\\[FILENAME: (.*?)\\](.*?)(?=\\[FILENAME: |$)", content, re.DOTALL)

if files:
    for name, code in files:
        with open(os.path.join(work_dir, name.strip()), "w", encoding="utf-8") as f:
            f.write(code.strip())
    print(f"{{AGENT_NAME}} completed task and built {{len(files)}} files.")
else:
    with open(os.path.join(work_dir, "output.txt"), "w", encoding="utf-8") as f:
        f.write(content)
''')
    print(f"Generated {filename}")