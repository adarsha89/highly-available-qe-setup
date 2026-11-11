import os
import sys

# Ensure backend and current dir are in python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("TRACKER_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
