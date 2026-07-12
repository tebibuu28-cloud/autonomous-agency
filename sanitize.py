import os
import re

def sanitize_agent_output(agent_name):
    work_dir = f"work_{agent_name.lower().replace(' ', '_')}"
    file_path = os.path.join(work_dir, "output.txt")
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ASCII 96 is backtick
        bt = chr(96) * 3
        pattern = bt + r"(?:html|python|css)?\n(.*?)\n" + bt
        code_blocks = re.findall(pattern, content, re.DOTALL)
        
        if code_blocks:
            with open(os.path.join(work_dir, "sanitized_code.html"), "w", encoding='utf-8') as f:
                f.write("\n".join(code_blocks))
            print("Sanitized code saved.")
        else:
            print("Error: No code blocks found.")

if __name__ == "__main__":
    sanitize_agent_output("frontend_engineer")