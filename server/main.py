from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.builder import WidgetBuilder
from config.mcp_server import WidgetMCPServer
from tools import PizzaMapTool, PizzaListTool
import uvicorn

PROJECT_ROOT = Path(__file__).parent.parent

# 1. 빌드
builder = WidgetBuilder(PROJECT_ROOT)
build_results = builder.build_all()

# 2. Tools 초기화
tools = [
    PizzaMapTool(build_results["pizza-map"]),
    PizzaListTool(build_results["pizza-list"]),
]

# 3. 서버 실행
server = WidgetMCPServer(name="pizzaz-framework", widgets=tools)
app = server.get_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

