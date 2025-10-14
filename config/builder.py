import subprocess
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Dict


@dataclass
class WidgetBuildResult:
    name: str
    hash: str
    html: str


class WidgetBuilder:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.assets_dir = project_root / "assets"
    
    def build_all(self) -> Dict[str, WidgetBuildResult]:
        subprocess.run(["npx", "tsx", "build-all.mts"], cwd=self.project_root, check=True)
        return self._parse_build_results()
    
    def _parse_build_results(self) -> Dict[str, WidgetBuildResult]:
        results = {}
        for html_file in self.assets_dir.glob("*-*.html"):
            match = re.match(r"(.+)-([0-9a-f]{4})\.html$", html_file.name)
            if match:
                name, hash_val = match.groups()
                results[name] = WidgetBuildResult(
                    name=name,
                    hash=hash_val,
                    html=html_file.read_text()
                )
        return results

