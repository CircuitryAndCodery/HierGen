import json
from pathlib import Path

print(json.loads(Path(".coverage.json").read_text())["totals"]["percent_covered_display"], end="")
