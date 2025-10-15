#!/usr/bin/env python3
"""Test actual MCP server responses to verify widget metadata is included"""

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from mcp import types
from server.main import server

async def test_list_tools():
    """Test the list_tools endpoint"""
    print("=" * 60)
    print("TEST: list_tools")
    print("=" * 60)
    
    # Access the MCP server directly
    mcp_server = server.mcp._mcp_server
    
    # Create a list tools request
    request = types.ListToolsRequest(method="tools/list", params={})
    
    # Call the handler
    handler = mcp_server.request_handlers.get(types.ListToolsRequest)
    result = await handler(request)
    
    # Extract actual result from ServerResult
    tool_list = result.root if isinstance(result, types.ServerResult) else result
    
    print(f"\nFound {len(tool_list.tools)} tools:\n")
    
    for tool in tool_list.tools:
        print(f"Tool: {tool.name}")
        print(f"  Title: {tool.title if hasattr(tool, 'title') else 'N/A'}")
        print(f"  Description: {tool.description}")
        print(f"  Input Schema keys: {list(tool.inputSchema.keys())}")
        
        # Debug: print all attributes
        print(f"  DEBUG - Tool attributes: {dir(tool)}")
        print(f"  DEBUG - Tool dict: {tool.model_dump()}")
        
        # Check for _meta attribute safely
        meta = getattr(tool, '_meta', None)
        if meta:
            print(f"  ✓ Metadata keys: {list(meta.keys())}")
            for key, value in meta.items():
                if key.startswith("openai"):
                    print(f"    {key}: {value}")
        else:
            print(f"  ⚠️  No metadata found!")
        print()


async def test_call_tool():
    """Test calling a tool and check the response"""
    print("=" * 60)
    print("TEST: call_tool (pizza-list)")
    print("=" * 60)
    
    mcp_server = server.mcp._mcp_server
    
    # Create a call tool request
    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(
            name="pizza-list",
            arguments={"pizzaTopping": "pepperoni"}
        )
    )
    
    # Call the handler
    handler = mcp_server.request_handlers.get(types.CallToolRequest)
    result = await handler(request)
    
    print(f"\nResult type: {type(result)}")
    print(f"Result.root type: {type(result.root)}")
    
    if isinstance(result.root, types.CallToolResult):
        tool_result = result.root
        
        print(f"\nContent:")
        for content in tool_result.content:
            if isinstance(content, types.TextContent):
                print(f"  Text: {content.text}")
        
        print(f"\nStructured Content:")
        if tool_result.structuredContent:
            print(f"  {json.dumps(tool_result.structuredContent, indent=2)}")
        
        print(f"\nDEBUG - CallToolResult dict:")
        print(f"  {json.dumps(tool_result.model_dump(), indent=2)}")
        
        print(f"\nMetadata:")
        meta = getattr(tool_result, '_meta', None)
        if meta:
            print(f"  Metadata keys: {list(meta.keys())}")
            
            # Check for widget metadata
            if "openai.com/widget" in meta:
                print(f"  ✓ Widget metadata found!")
                widget_meta = meta["openai.com/widget"]
                print(f"    Resource type: {widget_meta.get('type')}")
                if 'resource' in widget_meta:
                    res = widget_meta['resource']
                    print(f"    Resource URI: {res.get('uri')}")
                    print(f"    Resource MIME: {res.get('mimeType')}")
                    print(f"    Resource title: {res.get('title')}")
                    html_len = len(res.get('text', ''))
                    print(f"    HTML length: {html_len} bytes")
            else:
                print(f"  ❌ NO widget metadata in response!")
            
            # Check other OpenAI metadata
            for key in meta.keys():
                if key.startswith("openai") and key != "openai.com/widget":
                    print(f"  {key}: {meta[key]}")
        else:
            print(f"  ❌ NO metadata in response!")


async def test_list_resources():
    """Test the list_resources endpoint"""
    print("\n" + "=" * 60)
    print("TEST: list_resources")
    print("=" * 60)
    
    mcp_server = server.mcp._mcp_server
    
    request = types.ListResourcesRequest(method="resources/list", params={})
    handler = mcp_server.request_handlers.get(types.ListResourcesRequest)
    result = await handler(request)
    
    # Extract actual result from ServerResult
    resource_list = result.root if isinstance(result, types.ServerResult) else result
    
    print(f"\nFound {len(resource_list.resources)} resources:\n")
    
    for resource in resource_list.resources:
        print(f"Resource: {resource.name}")
        print(f"  URI: {resource.uri}")
        print(f"  MIME type: {resource.mimeType}")
        
        meta = getattr(resource, '_meta', None)
        if meta:
            print(f"  Metadata: {json.dumps(meta, indent=4)}")
        else:
            print(f"  No metadata")
        print()


async def test_read_resource():
    """Test reading a specific resource"""
    print("=" * 60)
    print("TEST: read_resource (pizza-list)")
    print("=" * 60)
    
    mcp_server = server.mcp._mcp_server
    
    request = types.ReadResourceRequest(
        method="resources/read",
        params=types.ReadResourceRequestParams(
            uri="ui://widget/pizza-list.html"
        )
    )
    
    handler = mcp_server.request_handlers.get(types.ReadResourceRequest)
    result = await handler(request)
    
    print(f"\nResult type: {type(result)}")
    print(f"Result.root type: {type(result.root)}")
    
    if isinstance(result.root, types.ReadResourceResult):
        print(f"Contents count: {len(result.root.contents)}")
        
        for i, content in enumerate(result.root.contents):
            print(f"\nContent {i}:")
            print(f"  Type: {type(content)}")
            print(f"  URI: {content.uri}")
            print(f"  MIME type: {content.mimeType}")
            print(f"  Text length: {len(content.text)} bytes")
            
            meta = getattr(content, '_meta', None)
            if meta:
                print(f"  Metadata: {json.dumps(meta, indent=4)}")


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MCP SERVER RESPONSE TEST")
    print("=" * 60 + "\n")
    
    try:
        await test_list_tools()
        await test_call_tool()
        await test_list_resources()
        await test_read_resource()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR!")
        print("=" * 60)
        print(f"\nError: {type(e).__name__}: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

