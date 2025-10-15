#!/usr/bin/env python3
"""Test script to verify all widgets are returning components correctly"""

import asyncio
from pathlib import Path
import sys
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config.builder import WidgetBuilder
from server.tools import PizzaMapTool, PizzaListTool

PROJECT_ROOT = Path(__file__).parent

def test_build_results():
    """Test that build process completes and returns expected widgets"""
    print("=" * 60)
    print("TEST 1: Build Process")
    print("=" * 60)
    
    builder = WidgetBuilder(PROJECT_ROOT)
    build_results = builder.build_all()
    
    print(f"✓ Build completed successfully")
    print(f"✓ Found {len(build_results)} widgets:")
    for name, result in build_results.items():
        print(f"  - {name} (hash: {result.hash}, html size: {len(result.html)} bytes)")
    
    # Check expected widgets exist
    expected_widgets = ["pizza_list", "pizza_map"]
    for widget_name in expected_widgets:
        assert widget_name in build_results, f"Missing widget: {widget_name}"
        assert build_results[widget_name].html, f"Empty HTML for {widget_name}"
        assert len(build_results[widget_name].html) > 100, f"HTML too small for {widget_name}"
        print(f"✓ {widget_name} has valid HTML content")
    
    print()
    return build_results


def test_tool_initialization(build_results):
    """Test that tools initialize correctly with build results"""
    print("=" * 60)
    print("TEST 2: Tool Initialization")
    print("=" * 60)
    
    tools = [
        PizzaMapTool(build_results["pizza_map"]),
        PizzaListTool(build_results["pizza_list"]),
    ]
    
    for tool in tools:
        print(f"\nTesting {tool.__class__.__name__}:")
        print(f"  ✓ Identifier: {tool.identifier}")
        print(f"  ✓ Title: {tool.title}")
        print(f"  ✓ Template URI: {tool.template_uri}")
        print(f"  ✓ Build result attached: {tool.build_result is not None}")
        print(f"  ✓ HTML size: {len(tool.build_result.html)} bytes")
        
        # Check HTML contains React root
        expected_root = f'id="{tool.build_result.name}-root"'
        assert expected_root in tool.build_result.html, f"Missing root div for {tool.identifier}"
        print(f"  ✓ HTML contains root element: {expected_root}")
    
    print()
    return tools


def test_embedded_resources(tools):
    """Test that embedded resources are structured correctly"""
    print("=" * 60)
    print("TEST 3: Embedded Resources")
    print("=" * 60)
    
    for tool in tools:
        print(f"\nTesting {tool.__class__.__name__} embedded resource:")
        
        resource = tool.get_embedded_resource()
        
        assert resource.type == "resource", f"Wrong type: {resource.type}"
        print(f"  ✓ Type: {resource.type}")
        
        assert str(resource.resource.uri) == str(tool.template_uri), f"URI mismatch: expected {tool.template_uri}, got {resource.resource.uri}"
        print(f"  ✓ URI: {resource.resource.uri}")
        
        assert resource.resource.mimeType == "text/html+skybridge", "Wrong mime type"
        print(f"  ✓ MIME type: {resource.resource.mimeType}")
        
        assert resource.resource.text == tool.build_result.html, "HTML mismatch"
        print(f"  ✓ HTML matches build result ({len(resource.resource.text)} bytes)")
        
        assert resource.resource.title == tool.title, "Title mismatch"
        print(f"  ✓ Title: {resource.resource.title}")
        
        # Check metadata
        meta = tool.get_resource_meta()
        print(f"  ✓ Resource metadata: {json.dumps(meta, indent=4)}")
    
    print()


def test_tool_metadata(tools):
    """Test that tool metadata is structured correctly"""
    print("=" * 60)
    print("TEST 4: Tool Metadata")
    print("=" * 60)
    
    for tool in tools:
        print(f"\nTesting {tool.__class__.__name__} metadata:")
        
        meta = tool.get_tool_meta()
        
        assert "openai/outputTemplate" in meta, "Missing outputTemplate"
        assert meta["openai/outputTemplate"] == tool.template_uri
        print(f"  ✓ Output template: {meta['openai/outputTemplate']}")
        
        assert "openai/widgetAccessible" in meta
        print(f"  ✓ Widget accessible: {meta['openai/widgetAccessible']}")
        
        assert "openai/resultCanProduceWidget" in meta
        assert meta["openai/resultCanProduceWidget"] is True
        print(f"  ✓ Result can produce widget: True")
        
        assert "openai/toolInvocation/invoking" in meta
        print(f"  ✓ Invoking message: '{meta['openai/toolInvocation/invoking']}'")
        
        assert "openai/toolInvocation/invoked" in meta
        print(f"  ✓ Invoked message: '{meta['openai/toolInvocation/invoked']}'")
    
    print()


async def test_tool_execution(tools):
    """Test that tools can execute and return proper data"""
    print("=" * 60)
    print("TEST 5: Tool Execution")
    print("=" * 60)
    
    # Test PizzaListTool
    pizza_list_tool = next(t for t in tools if isinstance(t, PizzaListTool))
    print(f"\nTesting {pizza_list_tool.__class__.__name__} execution:")
    
    from server.tools.pizza_list_tool import PizzaListInput
    input_data = PizzaListInput(pizzaTopping="pepperoni")
    result = await pizza_list_tool.execute(input_data)
    
    print(f"  ✓ Input: pizzaTopping='pepperoni'")
    print(f"  ✓ Result keys: {list(result.keys())}")
    assert "pizzaTopping" in result, "Missing pizzaTopping in result"
    assert "places" in result, "Missing places in result"
    print(f"  ✓ Returned {len(result['places'])} places")
    print(f"  ✓ Sample place: {result['places'][0] if result['places'] else 'None'}")
    
    # Test PizzaMapTool
    pizza_map_tool = next(t for t in tools if isinstance(t, PizzaMapTool))
    print(f"\nTesting {pizza_map_tool.__class__.__name__} execution:")
    
    from server.tools.pizza_map_tool import PizzaMapInput
    input_data = PizzaMapInput(pizzaTopping="margherita")
    result = await pizza_map_tool.execute(input_data)
    
    print(f"  ✓ Input: pizzaTopping='margherita'")
    print(f"  ✓ Result keys: {list(result.keys())}")
    assert "pizzaTopping" in result, "Missing pizzaTopping in result"
    assert "places" in result, "Missing places in result"
    print(f"  ✓ Returned {len(result['places'])} places")
    print(f"  ✓ Sample place: {result['places'][0] if result['places'] else 'None'}")
    
    print()


def test_html_content(tools):
    """Test that HTML content is valid and contains expected elements"""
    print("=" * 60)
    print("TEST 6: HTML Content Validation")
    print("=" * 60)
    
    for tool in tools:
        print(f"\nValidating {tool.__class__.__name__} HTML:")
        html = tool.build_result.html
        
        # Basic HTML structure
        assert "<!doctype html>" in html.lower(), "Missing doctype"
        assert "<html>" in html.lower(), "Missing html tag"
        assert "<body>" in html.lower(), "Missing body tag"
        print(f"  ✓ Valid HTML structure")
        
        # React root div
        root_id = f"{tool.build_result.name}-root"
        assert root_id in html, f"Missing root div with id {root_id}"
        print(f"  ✓ Contains React root: #{root_id}")
        
        # JavaScript module
        assert '<script type="module">' in html, "Missing module script"
        print(f"  ✓ Contains module script")
        
        # Check for React code indicators
        assert "react" in html.lower() or "jsx" in html.lower() or "createElement" in html, "No React code found"
        print(f"  ✓ Contains React code")
        
        # Check for useWidgetProps hook
        if "useWidgetProps" in html or "openai" in html:
            print(f"  ✓ Contains widget integration code")
    
    print()


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("WIDGET COMPONENT TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        # Run tests
        build_results = test_build_results()
        tools = test_tool_initialization(build_results)
        test_embedded_resources(tools)
        test_tool_metadata(tools)
        await test_tool_execution(tools)
        test_html_content(tools)
        
        # Summary
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nSummary:")
        print(f"  • {len(build_results)} widgets built successfully")
        print(f"  • {len(tools)} tools initialized correctly")
        print(f"  • All embedded resources properly configured")
        print(f"  • All tools can execute and return data")
        print(f"  • All HTML content is valid")
        print("\n✨ Your widgets are ready to be served!\n")
        
    except AssertionError as e:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED!")
        print("=" * 60)
        print(f"\nError: {e}\n")
        sys.exit(1)
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR!")
        print("=" * 60)
        print(f"\nError: {type(e).__name__}: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

