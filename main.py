"""
Universal-Market-Scanner Application Entrypoint.
"""

import sys
from cli import demo

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        import uvicorn
        uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000)
    else:
        demo()

if __name__ == "__main__":
    main()
