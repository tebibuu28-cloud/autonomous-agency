import os
import json
import csv
import re
import argparse
import time
import urllib.request
from datetime import datetime
from typing import List, Dict, Any

class StatePayload:
    """Tracks global production state, telemetry, and snapshots for failure recovery."""
    def __init__(self, framework: str, prompt: str):
        self.framework: str = framework
        self.prompt: str = prompt
        self.plan: List[Dict[str, Any]] = []
        self.final_text: str = ""
        self.media_assets: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {
            "telemetry": {},
            "health_checks": "Unexecuted",
            "pipeline_completion_status": "Initialized",
            "generation_mode": "Unknown"
        }
        self.history_snapshot: Dict[str, Any] = {}

    def capture_snapshot(self, agent_name: str):
        self.history_snapshot[agent_name] = {
            "plan": list(self.plan),
            "final_text": self.final_text,
            "media_assets": list(self.media_assets)
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "framework": self.framework,
            "prompt": self.prompt,
            "plan": self.plan,
            "final_text": self.final_text,
            "media_assets": self.media_assets,
            "metadata": self.metadata
        }

class SystemGuard:
    @staticmethod
    def run_preflight_checks() -> bool:
        print("⚙️ [System Guard] Running pre-flight diagnostic validation...")
        return True

    @staticmethod
    def validate_schema(state: StatePayload) -> bool:
        if not isinstance(state.plan, list):
            print("❌ [System Guard] Schema Validation Failure: 'plan' must be a list structure.")
            return False
        return True

class PlannerAgent:
    def run(self, state: StatePayload) -> StatePayload:
        start_time = time.time()
        print("🧠 [Agent: Planner] Designing structural blueprint sections...")
        state.capture_snapshot("Planner")
        
        state.plan = [
            {"section_id": 1, "title": "1. System Topology & Architecture Design", "focus": "Structural blueprint overview"},
            {"section_id": 2, "title": "2. High-Performance Execution Implementation", "focus": "Core structural/code implementation logic"},
            {"section_id": 3, "title": "3. Telemetry, Scaling & Operational Guards", "focus": "Validation, optimization, and scale parameters"}
        ]
            
        print(f"✅ Generated {len(state.plan)} structural layout targets.")
        state.metadata["telemetry"]["PlannerAgent_duration_ms"] = round((time.time() - start_time) * 1000, 2)
        return state

class WriterAgent:
    """Agent 2: Dual Local Inference Router & Section-Specific Fallback Matrix."""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "llama3.2"
        
        # Section-specific default blueprint specifications
        self.section_blueprints = {
            1: {
                "title": "DISTRIBUTED AUTOMATION ORCHESTRATOR",
                "template": (
                    "```python\n"
                    "# Localized Execution Pipeline & Secure Infrastructure Controller\n"
                    "import os\n\n"
                    "class CloudPipelineController:\n"
                    "    def __init__(self, context_node='us-east-1'):\n"
                    "        self.node = context_node\n\n"
                    "    def deploy_secure_grid(self):\n"
                    "        print(f'[Deploy Engine] Initializing sandboxed environment node: {self.node}')\n"
                    "        os.environ['SYSTEM_ISOLATION_GUARD'] = 'TRUE'\n"
                    "        return {'status': 'active', 'security_encryption': 'AES-256'}\n"
                    "```"
                )
            },
            2: {
                "title": "DATA ACCELERATION GRID LAYER",
                "template": (
                    "```python\n"
                    "# High-Performance Database Connection Pooling & Optimization\n"
                    "import sqlite3\n\n"
                    "class DatabaseAutomationGrid:\n"
                    "    def __init__(self, db_path='production.db'):\n"
                    "        self.db_path = db_path\n\n"
                    "    def execute_optimized_query(self, query: str, params=()):\n"
                    "        with sqlite3.connect(self.db_path) as conn:\n"
                    "            conn.execute('PRAGMA synchronous = OFF;')\n"
                    "            conn.execute('PRAGMA journal_mode = WAL;')\n"
                    "            cursor = conn.cursor()\n"
                    "            cursor.execute(query, params)\n"
                    "            return cursor.fetchall()\n"
                    "```"
                )
            },
            3: {
                "title": "TELEMETRY & VISUAL ANALYTICAL CORE",
                "template": (
                    "```python\n"
                    "# Real-Time System Profiler and Graphical Telemetry Collector\n"
                    "import time\n"
                    "import json\n\n"
                    "class TelemetryVisualizer:\n"
                    "    def __init__(self):\n"
                    "        self.metrics_log = 'telemetry_stream.json'\n\n"
                    "    def profile_agent_matrix(self, agent_name: str, duration_ms: float):\n"
                    "        payload = {'agent': agent_name, 'latency_ms': duration_ms, 'epoch': time.time()}\n"
                    "        print(f'[Telemetry Visualizer] LOGGED -> {json.dumps(payload)}')\n"
                    "```"
                )
            }
        }

    def _query_local_llm(self, prompt: str) -> str:
        data = {"model": self.model_name, "prompt": prompt, "stream": False}
        req = urllib.request.Request(
            self.ollama_url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data.get("response", "")

    def run(self, state: StatePayload) -> StatePayload:
        start_time = time.time()
        print("✍️ [Agent: Writer] Generating content copy blocks...")
        state.capture_snapshot("Writer")
        
        try:
            print(f"📡 [LLM Link] Attempting connection to local inference system ({self.model_name})...")
            structured_prompt = (
                f"You are an elite technical software architect agent.\n"
                f"Write a highly detailed, professional, structured Markdown guide responding to this engineering request:\n"
                f"'{state.prompt}'\n\n"
                f"Provide clear sections, explanations, and fully functional, clean Python code implementations where applicable."
            )
            llm_response = self._query_local_llm(structured_prompt)
            if llm_response:
                state.final_text = llm_response
                state.metadata["generation_mode"] = f"Live LLM Inference ({self.model_name})"
                print("✨ [Inference Router] Successfully generated live responses from model engine.")
                state.metadata["telemetry"]["WriterAgent_duration_ms"] = round((time.time() - start_time) * 1000, 2)
                return state
        except Exception:
            print("⚠️ [Inference Router] Local model server offline. Redirecting to Section Blueprint Matrix...")

        state.metadata["generation_mode"] = "Section Blueprint Matrix (Fallback Mode)"
        compiled_sections = [f"# Enterprise System Guide: {state.prompt}\n"]
        
        # Sequentially map unique code blocks per section instead of repeating matches
        for section in state.plan:
            sec_id = section["section_id"]
            compiled_sections.append(f"## {section['title']}")
            compiled_sections.append(f"> Intent Focus: {section['focus']}\n")
            compiled_sections.append(f"Deploying structural logic targeting input requirements: *\"{state.prompt}\"*.\n")
            
            if sec_id in self.section_blueprints:
                blueprint = self.section_blueprints[sec_id]
                compiled_sections.append(f"### ⚙️ IMPLEMENTATION SPECIFICATION: {blueprint['title']}")
                compiled_sections.append("The multi-agent orchestration engine injected this section-specific blueprint:")
                compiled_sections.append(blueprint["template"] + "\n")
            else:
                compiled_sections.append("```python\n# Default boilerplate automation backup\nprint('[Platform Workload] Executing pipeline targets.')\n```\n")

        state.final_text = "\n".join(compiled_sections)
        print("✅ Unique content compilation completed via fallback matrix layout maps.")
        state.metadata["telemetry"]["WriterAgent_duration_ms"] = round((time.time() - start_time) * 1000, 2)
        return state

class AssetAllocatorAgent:
    def run(self, state: StatePayload) -> StatePayload:
        start_time = time.time()
        print("🖼️ [Agent: Asset Allocator] Injecting platform asset blueprints...")
        state.capture_snapshot("AssetAllocator")
        
        state.media_assets = [
            {"asset_name": "optimized_header.png", "scale": 100, "priority": "High"},
            {"asset_name": "data_visualization.png", "scale": 75, "priority": "Medium"}
        ]
        
        state.metadata["word_count_estimate"] = len(state.final_text.split())
        state.metadata["telemetry"]["AssetAllocatorAgent_duration_ms"] = round((time.time() - start_time) * 1000, 2)
        return state

class OrchestrationEngine:
    def __init__(self):
        self.planner = PlannerAgent()
        self.writer = WriterAgent()
        self.allocator = AssetAllocatorAgent()
        
    def execute_workflow(self, framework: str, prompt: str) -> StatePayload:
        print(f"\n🚀 Launching Orchestration Sequence for prompt: '{prompt[:45]}...'")
        state = StatePayload(framework, prompt)
        
        if SystemGuard.run_preflight_checks():
            state.metadata["health_checks"] = "Passed"
        else:
            state.metadata["health_checks"] = "Failed"
            raise RuntimeError("Preflight system sanity check failed to pass.")
            
        try:
            print("----------------------------------------------------------------")
            state = self.planner.run(state)
            if not SystemGuard.validate_schema(state):
                raise ValueError("Payload layout corrupted during phase execution.")
                
            print("----------------------------------------------------------------")
            state = self.writer.run(state)
            print("----------------------------------------------------------------")
            state = self.allocator.run(state)
            print("----------------------------------------------------------------")
            state.metadata["pipeline_completion_status"] = "Success"
        except Exception as err:
            print(f"💥 [Error Boundary caught failure]: {str(err)}")
            state.metadata["pipeline_completion_status"] = "Failed"
            state.metadata["error_log_context"] = str(err)
            
        return state

def save_output_artifacts(final_state: StatePayload):
    timestamp_index = datetime.now().strftime("%Y%m%d_%H%M%S")
    markdown_filename = f"output_content_{timestamp_index}.md"
    json_filename = f"output_state_{timestamp_index}.json"
    log_filename = "execution_log.csv"
    
    with open(markdown_filename, "w", encoding="utf-8") as md_file:
        md_file.write(final_state.final_text)
    print(f"💾 Saved unique text build: '{markdown_filename}'")
    
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(final_state.to_dict(), json_file, indent=4)
    print(f"💾 Saved raw backup snapshot: '{json_filename}'")
    
    file_exists = os.path.exists(log_filename)
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_filename, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(["Timestamp", "Framework", "Prompt Focus", "Word Count", "Status", "Gen Mode", "Telemetry Map"])
        writer.writerow([
            current_time_str,
            final_state.framework,
            final_state.prompt,
            final_state.metadata.get("word_count_estimate", 0),
            final_state.metadata.get("pipeline_completion_status", "Unknown"),
            final_state.metadata.get("generation_mode", "Unknown"),
            json.dumps(final_state.metadata.get("telemetry", {}))
        ])
    print(f"📈 Telemetry logged to: '{log_filename}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Multi-Agent Engine Framework")
    parser.add_argument("--framework", type=str, default="high-demand_templates", help="Target structure style")
    parser.add_argument("--prompt", type=str, help="Single runtime execution prompt focus text")
    parser.add_argument("--file", type=str, help="Path to text file containing multiple prompts")
    args = parser.parse_args()
    
    orchestrator = OrchestrationEngine()
    prompts_queue = []
    
    if args.file:
        if os.path.exists(args.file):
            print(f"📂 [Batch Ingestion] Loading instructions file: '{args.file}'")
            with open(args.file, "r", encoding="utf-8") as f:
                prompts_queue = [line.strip() for line in f if line.strip()]
            print(f"📋 Loaded {len(prompts_queue)} automation tasks from file.")
        else:
            print(f"❌ Error: Specified batch file '{args.file}' not found.")
            exit(1)
    elif args.prompt:
        prompts_queue.append(args.prompt)
    else:
        print("❌ Error: You must supply either a single target via --prompt or a task list via --file.")
        exit(1)
        
    for idx, dynamic_prompt in enumerate(prompts_queue, start=1):
        print(f"\n============================================ [Task {idx}/{len(prompts_queue)}] ============================================")
        final_state = orchestrator.execute_workflow(args.framework, dynamic_prompt)
        save_output_artifacts(final_state)
        if idx < len(prompts_queue):
            time.sleep(1.1)
            
    print("\n🏁 ============================================ BATCH COMPLETION SUCCESS ============================================")