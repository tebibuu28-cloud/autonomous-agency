@echo off
title Multi-Agent Enterprise Engine - Setup Wizard
echo ================================================================
echo 🚀 INITIALIZING MULTI-AGENT AGENCY REPOSITORY SETUP
echo ================================================================

echo 📦 1. Verifying Local Python Environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not added to system PATH.
    pause
    exit /b
)

echo ✅ 2. Creating Isolated Virtual Environment (.venv)...
python -m venv .venv

echo ⚙️ 3. Activating Environment and Upgrading Package Managers...
call .venv\Scripts\activate.bat

echo 📥 4. Installing Production Dependency Grid...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo 🛠️ 5. Running Preflight Verification Diagnostics...
python app.py --prompt "System initialization health check run"

echo ================================================================
echo 🎉 REPOSITORY SETUP COMPLETELY SUCCESSFUL!
echo ================================================================
echo To activate the engine in the future, run: call .venv\Scripts\activate
pause