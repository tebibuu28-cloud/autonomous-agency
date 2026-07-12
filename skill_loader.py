import os
import subprocess

skills_map = {
    "trading": "https://github.com/ccxt/ccxt",
    "security": "https://github.com/PyCQA/bandit",
    "backend": "https://github.com/tiangolo/fastapi"
}

def clone_skills():
    base_path = r'C:\Users\tebibu\.gemini\antigravity\scratch\agent_company\skills'
    os.makedirs(base_path, exist_ok=True)
    
    for category, url in skills_map.items():
        dest = os.path.join(base_path, category)
        # Check if the folder exists to avoid duplicate errors
        if not os.path.exists(dest):
            print(f"Attempting shallow clone for {category}...")
            try:
                # --depth 1 creates a 'shallow' clone to avoid large data transfers
                subprocess.run(["git", "clone", "--depth", "1", url, dest], check=True)
                print(f"Successfully learned skills from {category}")
            except subprocess.CalledProcessError:
                print(f"Failed to clone {category}. Check your internet connection.")
        else:
            print(f"Skills for {category} already exist.")

if __name__ == "__main__":
    clone_skills()