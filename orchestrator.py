import subprocess
import os

def run_step(agent, task):
    """Executes a specific agent task via the dispatcher."""
    print(f"\n[ORCHESTRATOR] Dispatching: {agent}")
    print(f"[TASK] {task}")
    subprocess.run(["python", "dispatcher.py", agent, task], check=True)

def sanitize_output(agent_name):
    """Calls your existing sanitizer script."""
    print(f"\n[ORCHESTRATOR] Sanitizing output for {agent_name}...")
    subprocess.run(["python", "sanitize.py"], check=True)

def run_landing_page_pipeline():
    """The automated workflow for your GitHub repository landing page."""
    
    # Step 1: Generate Content
    run_step("brand_strategist", "Create compelling text for my GitHub repo landing page. Include: Value prop, key features, and a CTA button text.")
    
    # Step 2: Generate Frontend Code
    run_step("frontend_engineer", "Read the output from the brand_strategist and write a professional, responsive HTML landing page. Output ONLY the code.")
    
    # Step 3: Clean the result
    sanitize_output("frontend_engineer")
    
    print("\n--- WORKFLOW COMPLETE ---")
    print("Your production-ready code is located in: work_frontend_engineer/sanitized_code.html")

if __name__ == "__main__":
    # Ensure all directories exist before starting
    if not os.path.exists("work_brand_strategist"): os.makedirs("work_brand_strategist")
    if not os.path.exists("work_frontend_engineer"): os.makedirs("work_frontend_engineer")
    
    run_landing_page_pipeline()