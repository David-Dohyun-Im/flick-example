#!/usr/bin/env python3
"""Final validation that widget metadata is properly included in MCP responses"""

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from mcp import types
from server.main import server

async def main():
    print("\n" + "=" * 70)
    print("FINAL WIDGET METADATA VALIDATION")
    print("=" * 70 + "\n")
    
    mcp_server = server.mcp._mcp_server
    
    # Test call_tool response
    print("Testing pizza-list tool call...")
    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(
            name="pizza-list",
            arguments={"pizzaTopping": "pepperoni"}
        )
    )
    
    handler = mcp_server.request_handlers.get(types.CallToolRequest)
    result = await handler(request)
    
    # Serialize to JSON (as it would be sent over the wire)
    result_dict = result.model_dump()
    tool_result_dict = result_dict
    
    print(f"\n✅ Tool executed successfully!")
    print(f"   Text response: {result.root.content[0].text}")
    print(f"   Structured content keys: {list(result.root.structuredContent.keys())}")
    
    # Check metadata
    if 'meta' in result_dict:
        print(f"\n✅ Metadata present in response!")
        meta = result_dict['meta']
        print(f"   Metadata keys: {list(meta.keys())}")
        
        # Check for widget metadata
        if 'openai.com/widget' in meta:
            print(f"\n✅ Widget metadata found!")
            widget_meta = meta['openai.com/widget']
            print(f"   Resource type: {widget_meta['type']}")
            print(f"   Resource URI: {widget_meta['resource']['uri']}")
            print(f"   Resource MIME: {widget_meta['resource']['mimeType']}")
            print(f"   HTML length: {len(widget_meta['resource']['text'])} bytes")
            print(f"   Widget title: {widget_meta['resource']['title']}")
        else:
            print(f"\n❌ No openai.com/widget in metadata!")
            sys.exit(1)
        
        # Check other OpenAI metadata
        required_keys = [
            'openai/outputTemplate',
            'openai/toolInvocation/invoking',
            'openai/toolInvocation/invoked',
            'openai/widgetAccessible',
            'openai/resultCanProduceWidget'
        ]
        
        print(f"\n✅ Checking required OpenAI metadata fields...")
        for key in required_keys:
            if key in meta:
                print(f"   ✓ {key}: {meta[key]}")
            else:
                print(f"   ❌ Missing: {key}")
                sys.exit(1)
    else:
        print(f"\n❌ No metadata in response!")
        sys.exit(1)
    
    # Test list_tools
    print(f"\n" + "=" * 70)
    print("Testing list_tools...")
    request = types.ListToolsRequest(method="tools/list", params={})
    handler = mcp_server.request_handlers.get(types.ListToolsRequest)
    result = await handler(request)
    
    tool_list = result.root if isinstance(result, types.ServerResult) else result
    tools_dict = [t.model_dump() for t in tool_list.tools]
    
    print(f"✅ Found {len(tools_dict)} tools")
    for tool_dict in tools_dict:
        print(f"\n   Tool: {tool_dict['name']}")
        print(f"   Title: {tool_dict.get('title', 'N/A')}")
        if 'meta' in tool_dict:
            print(f"   ✓ Has metadata with keys: {list(tool_dict['meta'].keys())}")
        else:
            print(f"   ⚠️  No metadata (this is OK for list_tools)")
    
    print(f"\n" + "=" * 70)
    print("🎉 ALL VALIDATIONS PASSED!")
    print("=" * 70)
    print("\nYour MCP server is correctly configured to serve widgets!")
    print("The widgets will display properly in ChatGPT when the tool is called.\n")

if __name__ == "__main__":
    asyncio.run(main())

