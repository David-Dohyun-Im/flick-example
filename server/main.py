from pathlib import Path
import sys
import importlib
import inspect

# Add parent directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import Flicky framework
from flicky import WidgetBuilder, WidgetMCPServer, BaseWidget
import uvicorn

PROJECT_ROOT = Path(__file__).parent.parent
TOOLS_DIR = Path(__file__).parent / "tools"


def auto_load_tools(build_results):
    """tools 디렉토리에서 자동으로 Tool 클래스들을 로드"""
    tools = []
    
    # tools 디렉토리의 모든 Python 파일 스캔
    for tool_file in TOOLS_DIR.glob("*_tool.py"):
        module_name = tool_file.stem
        
        try:
            # 동적으로 모듈 import
            module = importlib.import_module(f"server.tools.{module_name}")
            
            # 모듈에서 BaseWidget을 상속받은 클래스 찾기
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseWidget) and obj is not BaseWidget:
                    # Tool의 identifier로 build_result 찾기
                    tool_identifier = obj.identifier
                    
                    if tool_identifier in build_results:
                        tool_instance = obj(build_results[tool_identifier])
                        tools.append(tool_instance)
                        print(f"✓ Loaded tool: {name} (identifier: {tool_identifier})")
                    else:
                        print(f"⚠ Warning: No build result found for tool '{tool_identifier}'")
        
        except Exception as e:
            print(f"✗ Error loading {tool_file.name}: {e}")
    
    return tools


# 1. 빌드
builder = WidgetBuilder(PROJECT_ROOT)
build_results = builder.build_all()

# 2. Tools 자동 로드
tools = auto_load_tools(build_results)

if not tools:
    print("⚠ No tools loaded!")

# 3. 서버 실행
server = WidgetMCPServer(name="pizzaz-framework", widgets=tools)
app = server.get_app()

if __name__ == "__main__":
    print(f"\n🚀 Starting server with {len(tools)} tools")
    uvicorn.run(app, host="0.0.0.0", port=8001)

