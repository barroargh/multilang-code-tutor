"""
Build the R Training Bot as a standalone Windows .exe using PyInstaller.

Run:
    pip install pyinstaller fastapi uvicorn anthropic openai ollama
    python build.py

Output: dist/R_Training_Bot.exe
"""

import PyInstaller.__main__
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SEP  = ";" if sys.platform == "win32" else ":"

PyInstaller.__main__.run([
    "server.py",
    "--name=R_Training_Bot",
    "--onefile",
    "--noconfirm",
    # Bundle static files and the system prompt
    f"--add-data={ROOT / 'static'}{SEP}static",
    f"--add-data={ROOT / 'system_prompt.md'}{SEP}.",
    # FastAPI / uvicorn hidden imports
    "--hidden-import=uvicorn.logging",
    "--hidden-import=uvicorn.loops",
    "--hidden-import=uvicorn.loops.auto",
    "--hidden-import=uvicorn.protocols",
    "--hidden-import=uvicorn.protocols.http",
    "--hidden-import=uvicorn.protocols.http.auto",
    "--hidden-import=uvicorn.protocols.websockets",
    "--hidden-import=uvicorn.protocols.websockets.auto",
    "--hidden-import=uvicorn.lifespan",
    "--hidden-import=uvicorn.lifespan.on",
    "--hidden-import=fastapi",
    "--hidden-import=anyio",
    "--hidden-import=anyio.lowlevel",
    "--hidden-import=anyio._backends._asyncio",
    "--hidden-import=starlette",
    "--hidden-import=starlette.routing",
    # LLM providers
    "--hidden-import=anthropic",
    "--hidden-import=openai",
    "--hidden-import=ollama",
    # Collect uvicorn & starlette fully (they use dynamic imports internally)
    "--collect-all=uvicorn",
    "--collect-all=starlette",
])

print("\nBuild complete — find R_Training_Bot.exe in the dist/ folder.")
print("Copy R_Training_Bot.exe to any Windows machine and double-click to run.")
print("No Python installation required on the target machine.")
