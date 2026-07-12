import subprocess
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('agent', help="The name of the agent file")
parser.add_argument('task', help="The task to perform")
args = parser.parse_args()

agent_file = f"{args.agent.lower().replace(' ', '_')}.py"
venv_python = r"C:\Users\tebibu\.gemini\antigravity\scratch\agent_company\venv\Scripts\python.exe"

if not os.path.exists(agent_file):
    print(f"Error: {agent_file} not found.")
else:
    try:
        subprocess.run([venv_python, agent_file, "--task", args.task], check=True)
    except Exception as e:
        print(f"Execution Error: {e}")