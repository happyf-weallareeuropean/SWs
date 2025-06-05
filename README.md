less decition yet always on right direct.

# SWs
software come to u: search via action not en discover. personize/customerze sw.

## Prototype

This repository includes a small prototype (`prototype.py`) that monitors
basic keyboard and mouse usage. After running for 60 seconds (or when you
press `ESC`), it prints a summary of actions and suggests potential
productivity tools.

### Run

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute the script:
   ```bash
   python prototype.py
   ```

The script listens for:
- `CMD+Tab` to detect frequent app switching.
- `CMD+Space` usage (Spotlight).
- Mouse drag actions that might indicate window resizing.

Based on these counts it prints simple recommendations such as trying
Raycast or using a window manager.
