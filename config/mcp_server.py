from typing import List, Any, Dict
from fastmcp import FastMCP
from mcp import types
from .base_widget import BaseWidget
from .handlers import MCPHandlers


class WidgetMCPServer:
    """FastMCP 기반 MCP 서버 래퍼"""
    
    def __init__(self, name: str, widgets: List[BaseWidget]):
        self.widgets_by_id = {w.identifier: w for w in widgets}
        self.widgets_by_uri = {w.template_uri: w for w in widgets}
        
        self.mcp = FastMCP(name=name)
        
        self.handlers = MCPHandlers(self.widgets_by_id, self.widgets_by_uri)
        self._register_tools_simple()
        self._register_resources()
        # TODO: 위젯 메타데이터 추가는 나중에 구현
        # self._setup_custom_call_handler()
    
    def _register_tools_simple(self):
        """FastMCP의 @tool 데코레이터 방식으로 도구 등록"""
        for widget in self.widgets_by_id.values():
            # Pydantic 모델의 필드 정보 가져오기
            schema = widget.input_schema.model_fields
            
            # exec를 사용하여 명시적인 파라미터를 가진 함수 생성
            # 파라미터 리스트 생성
            params = []
            for field_name, field_info in schema.items():
                type_name = field_info.annotation.__name__ if hasattr(field_info.annotation, '__name__') else 'Any'
                params.append(f"{field_name}: {type_name}")
            
            params_str = ", ".join(params)
            
            # 함수 코드 생성
            func_code = f'''
async def {widget.identifier.replace('-', '_')}({params_str}):
    """{widget.description or widget.title}"""
    # 파라미터를 딕셔너리로 수집
    args_dict = {{{", ".join(f'"{name}": {name}' for name in schema.keys())}}}
    # Pydantic 모델로 검증
    input_data = widget.input_schema.model_validate(args_dict)
    # 위젯 실행
    result = await widget.execute(input_data)
    return result
'''
            
            # 함수 실행을 위한 네임스페이스
            namespace = {
                'widget': widget,
                'Any': Any
            }
            
            # 타입 어노테이션 추가
            for field_name, field_info in schema.items():
                if hasattr(field_info.annotation, '__name__'):
                    namespace[field_info.annotation.__name__] = field_info.annotation
            
            # 함수 생성
            exec(func_code, namespace)
            tool_func = namespace[widget.identifier.replace('-', '_')]
            
            # @mcp.tool 데코레이터 적용
            self.mcp.tool(name=widget.identifier, description=widget.description or widget.title)(tool_func)
    
    def _setup_custom_call_handler(self):
        """call_tool 핸들러를 커스터마이징하여 위젯 메타데이터 추가"""
        server = self.mcp._mcp_server
        original_call_tool = server.request_handlers.get(types.CallToolRequest)
        
        async def custom_call_tool(request: types.CallToolRequest):
            # 원래 핸들러 호출
            result = await original_call_tool(request)
            
            # 위젯 정보가 있으면 메타데이터 추가
            widget = self.widgets_by_id.get(request.params.name)
            if widget and isinstance(result, types.ServerResult):
                tool_result = result.root
                if isinstance(tool_result, types.CallToolResult):
                    # 위젯 embedded resource 추가
                    widget_resource = widget.get_embedded_resource()
                    meta = tool_result._meta or {}
                    meta["openai.com/widget"] = widget_resource.model_dump(mode="json")
                    meta.update(widget.get_tool_meta())
                    tool_result._meta = meta
            
            return result
        
        server.request_handlers[types.CallToolRequest] = custom_call_tool
    
    def _register_resources(self):
        """리소스를 FastMCP에 등록"""
        for widget in self.widgets_by_id.values():
            # 클로저 문제 해결을 위한 factory
            def make_resource_func(w):
                async def resource_func():
                    return w.build_result.html
                return resource_func
            
            self.mcp.resource(
                uri=widget.template_uri,
                name=widget.title,
                description=f"{widget.title} widget markup",
                mime_type="text/html+skybridge"
            )(make_resource_func(widget))
    
    def _setup_custom_handlers(self):
        """커스텀 핸들러 설정 (call_tool의 응답 형식 커스터마이징)"""
        server = self.mcp._mcp_server
        # call_tool 핸들러를 커스텀 핸들러로 교체하여 위젯 메타데이터 포함
        original_call_tool = server.request_handlers[types.CallToolRequest]
        
        async def custom_call_tool(request: types.CallToolRequest):
            # 원래 핸들러 호출
            result = await original_call_tool(request)
            
            # 위젯 정보가 있으면 메타데이터 추가
            widget = self.widgets_by_id.get(request.params.name)
            if widget and isinstance(result, types.ServerResult):
                tool_result = result.root
                if isinstance(tool_result, types.CallToolResult):
                    # 위젯 embedded resource 추가
                    widget_resource = widget.get_embedded_resource()
                    meta = tool_result._meta or {}
                    meta["openai.com/widget"] = widget_resource.model_dump(mode="json")
                    meta.update(widget.get_tool_meta())
                    tool_result._meta = meta
            
            return result
        
        server.request_handlers[types.CallToolRequest] = custom_call_tool
    
    def get_app(self):
        """FastAPI 앱 반환 (CORS 포함)"""
        app = self.mcp.http_app()
        
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

