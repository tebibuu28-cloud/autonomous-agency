import subprocess
import os

def run_step(agent, task):
    print(f"\n[FACTORY] Dispatching: {agent}")
    subprocess.run(["python", "dispatcher.py", agent, task], check=True)

def factory_workflow():
    print("--- STARTING AUTONOMOUS FACTORY ---")
    
    # 1. Generate Strategy
    run_step("brand_strategist", "Create text for a repo landing page. Include: Value prop, key features, and CTA.")
    
    # 2. Build Code
    run_step("frontend_engineer", "Read brand_strategist output and write an HTML landing page. Output ONLY the code inside ```html ... ```")
    
    # 3. Sanitize (Clean Code)
    print("[FACTORY] Cleaning code...")
    subprocess.run(["python", "sanitize.py"], check=True)
    
    # 4. Publish to GitHub
    print("[FACTORY] Pushing to repository...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Factory: Automated Landing Page Update"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[FACTORY] SUCCESS: Landing page published.")
    except Exception as e:
        print(f"[FACTORY] Git Error: {e}")

if __name__ == "__main__":
    factory_workflow()