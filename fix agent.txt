import os
import shutil

template = "worker_template.py"
# This loops through your folder and overwrites every agent with the new, healthy code
for filename in os.listdir("."):
    if filename.endswith(".py") and filename not in ["worker_template.py", "initialize_all.py", "orchestrator.py", "dispatcher.py", "fix_agents.py"]:
        shutil.copy(template, filename)
        print(f"Fixed: {filename}")