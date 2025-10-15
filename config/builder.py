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
        self.widgets_dir = project_root / "widgets"
    
    def build_all(self) -> Dict[str, WidgetBuildResult]:
        # 1. 자동으로 필요한 파일들 생성
        self._auto_generate_widget_files()
        
        # 2. 빌드 실행
        subprocess.run(["npx", "tsx", "build-all.mts"], cwd=self.project_root, check=True)
        
        # 3. 결과 파싱
        return self._parse_build_results()
    
    def _auto_generate_widget_files(self):
        """
        위젯 디렉토리 검증
        
        이제 mounting 로직이 build-all.mts에 통합되어 있어서
        각 위젯에는 index.jsx만 있으면 됩니다!
        """
        widget_count = 0
        for widget_dir in self.widgets_dir.iterdir():
            if not widget_dir.is_dir() or widget_dir.name.startswith('.'):
                continue
            
            widget_name = widget_dir.name
            index_file = widget_dir / "index.jsx"
            
            # index.jsx가 있으면 카운트
            if index_file.exists():
                widget_count += 1
                print(f"✓ Found widget: {widget_name}")
        
        if widget_count > 0:
            print(f"\n📦 Ready to build {widget_count} widget(s)")
    
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

