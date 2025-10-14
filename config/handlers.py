from typing import Dict, List
from mcp import types
from pydantic import ValidationError
from .base_widget import BaseWidget


class MCPHandlers:
    def __init__(self, widgets_by_id: Dict, widgets_by_uri: Dict):
        self.widgets_by_id = widgets_by_id
        self.widgets_by_uri = widgets_by_uri
    
    async def list_tools(self) -> List[types.Tool]:
        return [
            types.Tool(
                name=w.identifier,
                title=w.title,
                description=w.description or w.title,
                inputSchema=w.get_input_schema(),
                _meta=w.get_tool_meta(),
            )
            for w in self.widgets_by_id.values()
        ]
    
    async def list_resources(self) -> List[types.Resource]:
        return [
            types.Resource(
                name=w.title,
                title=w.title,
                uri=w.template_uri,
                description=f"{w.title} widget markup",
                mimeType="text/html+skybridge",
                _meta=w.get_resource_meta(),
            )
            for w in self.widgets_by_id.values()
        ]
    
    async def list_resource_templates(self) -> List[types.ResourceTemplate]:
        return [
            types.ResourceTemplate(
                name=w.title,
                title=w.title,
                uriTemplate=w.template_uri,
                description=f"{w.title} widget markup",
                mimeType="text/html+skybridge",
                _meta=w.get_resource_meta(),
            )
            for w in self.widgets_by_id.values()
        ]
    
    async def read_resource(self, req: types.ReadResourceRequest) -> types.ServerResult:
        widget = self.widgets_by_uri.get(str(req.params.uri))
        if not widget:
            return types.ServerResult(
                types.ReadResourceResult(contents=[], _meta={"error": f"Unknown resource: {req.params.uri}"})
            )
        
        contents = [
            types.TextResourceContents(
                uri=widget.template_uri,
                mimeType="text/html+skybridge",
                text=widget.build_result.html,
                _meta=widget.get_resource_meta(),
            )
        ]
        return types.ServerResult(types.ReadResourceResult(contents=contents))
    
    async def call_tool(self, req: types.CallToolRequest) -> types.ServerResult:
        widget = self.widgets_by_id.get(req.params.name)
        if not widget:
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=f"Unknown tool: {req.params.name}")],
                    isError=True
                )
            )
        
        try:
            input_data = widget.input_schema.model_validate(req.params.arguments or {})
            result_data = await widget.execute(input_data)
        except ValidationError as exc:
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=f"Validation error: {exc.errors()}")],
                    isError=True
                )
            )
        except Exception as exc:
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=f"Error: {str(exc)}")],
                    isError=True
                )
            )
        
        # 공식 스펙: _meta["openai.com/widget"]에 embedded resource
        widget_resource = widget.get_embedded_resource()
        meta = {
            "openai.com/widget": widget_resource.model_dump(mode="json"),
            **widget.get_tool_meta()
        }
        
        return types.ServerResult(
            types.CallToolResult(
                content=[types.TextContent(type="text", text=widget.invoked)],
                structuredContent=result_data,
                _meta=meta,
            )
        )

