from typing import List
from fastmcp import FastMCP
from mcp import types
from .base_widget import BaseWidget
from .handlers import MCPHandlers


class WidgetMCPServer:
    """FastMCP 기반 MCP 서버 래퍼"""
    
    def __init__(self, name: str, widgets: List[BaseWidget]):
        self.widgets_by_id = {w.identifier: w for w in widgets}
        self.widgets_by_uri = {w.template_uri: w for w in widgets}
        
        self.mcp = FastMCP(
            name=name,
            sse_path="/mcp",
            message_path="/mcp/messages",
            stateless_http=True
        )
        
        self.handlers = MCPHandlers(self.widgets_by_id, self.widgets_by_uri)
        self._register_handlers()
    
    def _register_handlers(self):
        """MCP 핸들러 등록"""
        self.mcp._mcp_server.list_tools = self.handlers.list_tools
        self.mcp._mcp_server.list_resources = self.handlers.list_resources
        self.mcp._mcp_server.list_resource_templates = self.handlers.list_resource_templates
        self.mcp._mcp_server.request_handlers[types.CallToolRequest] = self.handlers.call_tool
        self.mcp._mcp_server.request_handlers[types.ReadResourceRequest] = self.handlers.read_resource
    
    def get_app(self):
        """FastAPI 앱 반환 (CORS 포함)"""
        app = self.mcp.streamable_http_app()
        
        # CORS 미들웨어 추가
        try:
            from starlette.middleware.cors import CORSMiddleware
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
                allow_credentials=False
            )
        except Exception:
            pass
        
        return app

