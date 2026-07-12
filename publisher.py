import subprocess
import os

def publish_to_github():
    print("\n[PUBLISHER] Pushing to GitHub...")
    try:
        # Assumes you have your Git remote configured
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update from Agent Factory"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[PUBLISHER] Success: Code pushed to repository.")
    except subprocess.CalledProcessError:
        print("[PUBLISHER] Error: Git push failed. Ensure your repo is initialized.")

if __name__ == "__main__":
    publish_to_github()