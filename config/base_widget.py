from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from pydantic import BaseModel
import mcp.types as types


class BaseWidget(ABC):
    identifier: str
    title: str
    input_schema: type[BaseModel]
    description: str = ""
    invoking: str = "Processing..."
    invoked: str = "Completed"
    
    # OpenAI 고급 옵션
    widget_accessible: bool = True
    widget_description: Optional[str] = None
    widget_csp: Optional[Dict[str, List[str]]] = None
    widget_prefers_border: bool = False
    read_only: bool = True
    
    def __init__(self, build_result: 'WidgetBuildResult'):
        self.build_result = build_result
        self.template_uri = f"ui://widget/{self.identifier}.html"
    
    @abstractmethod
    async def execute(self, input_data: BaseModel) -> Dict[str, Any]:
        pass
    
    def get_input_schema(self) -> Dict[str, Any]:
        """Pydantic 모델을 JSON Schema로 변환"""
        return self.input_schema.model_json_schema()
    
    def get_tool_meta(self) -> Dict[str, Any]:
        """Tool 메타데이터 (공식 스펙 준수)"""
        meta = {
            "openai/outputTemplate": self.template_uri,
            "openai/toolInvocation/invoking": self.invoking,
            "openai/toolInvocation/invoked": self.invoked,
            "openai/widgetAccessible": self.widget_accessible,
            "openai/resultCanProduceWidget": True,
            "annotations": {
                "readOnlyHint": self.read_only,
            }
        }
        # widgetDescription은 resource meta에만 포함 (여기서는 제거)
        return meta
    
    def get_resource_meta(self) -> Dict[str, Any]:
        """Resource 메타데이터 (CSP, border 설정)"""
        meta = {}
        if self.widget_csp:
            meta["openai/widgetCSP"] = self.widget_csp
        if self.widget_prefers_border:
            meta["openai/widgetPrefersBorder"] = True
        if self.widget_description:
            meta["openai/widgetDescription"] = self.widget_description
        return meta
    
    def get_embedded_resource(self) -> types.EmbeddedResource:
        """Tool 응답에 포함할 embedded resource"""
        return types.EmbeddedResource(
            type="resource",
            resource=types.TextResourceContents(
                uri=self.template_uri,
                mimeType="text/html+skybridge",
                text=self.build_result.html,
                title=self.title,
                _meta=self.get_resource_meta(),
            ),
        )

