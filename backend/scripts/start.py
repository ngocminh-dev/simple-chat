import uvicorn
import subprocess

subprocess.run(["pre-commit", "install"], check=False, capture_output=True)


def start():
    """Launch in watch mode"""
    uvicorn.run(
        app="portal.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs="portal",
    )
