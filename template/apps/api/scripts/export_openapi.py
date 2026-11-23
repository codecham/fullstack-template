"""Write the API's OpenAPI schema to a file, without starting the server.

Usage (from apps/api): uv run python -m scripts.export_openapi ../web/openapi.json
The frontend generates its typed API client from this file (`make api-types`).
"""

import json
import sys
from pathlib import Path

from app.main import app

output = Path(sys.argv[1])
output.write_text(json.dumps(app.openapi(), indent=2) + "\n")
print(f"OpenAPI schema written to {output}")
