# Flick - ChatGPT Widget Framework

A Python-based framework for building and deploying interactive widgets for ChatGPT using FastMCP, React, and Vite.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Virtual environment activated

### Installation

```bash
# Clone and navigate to project
cd /Users/yunhyeok/Desktop/flick/flick

# Install Python dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install Node dependencies
npm install
```

### Running the Server

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Build widgets (automatically happens on server start)
npm run build

# Start the MCP server
python server/main.py

# Server will be available at http://0.0.0.0:8001
```

## 📦 Project Structure

```
flick/
├── server/                 # Python MCP server
│   ├── main.py            # Server entry point
│   ├── api/               # API endpoints
│   │   └── pizzeria_api.py
│   └── tools/             # MCP tools (widgets)
│       ├── pizza_list_tool.py
│       └── pizza_map_tool.py
│
├── config/                # Framework configuration
│   ├── base_widget.py     # Base widget class
│   ├── builder.py         # Widget builder
│   ├── handlers.py        # MCP handlers
│   └── mcp_server.py      # MCP server wrapper
│
├── widgets/               # React widget components
│   ├── pizza_list/
│   │   ├── index.jsx      # Component definition
│   │   └── _app.jsx       # Component mounting
│   └── pizza_map/
│       ├── index.jsx
│       └── _app.jsx
│
├── hooks/                 # React hooks
│   ├── use-widget-props.ts
│   ├── use-widget-state.ts
│   └── use-openai-global.ts
│
├── assets/                # Built widget bundles
│   ├── pizza_list-{hash}.html
│   └── pizza_map-{hash}.html
│
├── build-all.mts          # Widget build script
├── package.json           # Node dependencies
└── requirements.txt       # Python dependencies
```

## 🛠️ Creating a New Widget

### 1. Create Widget Component

Create a new directory under `widgets/` with your component:

```bash
mkdir -p widgets/my_widget
```

Create `widgets/my_widget/index.jsx`:

```jsx
import React from 'react';
import { useWidgetProps } from '../../hooks/use-widget-props';

export default function MyWidget() {
  const props = useWidgetProps();
  
  // Debug logging
  React.useEffect(() => {
    console.log('MyWidget received props:', props);
  }, [props]);
  
  // Show loading state if no data
  if (!props.myData) {
    return (
      <div className="my-widget">
        <h2>Loading...</h2>
        <pre style={{ fontSize: '10px', background: '#f5f5f5', padding: '10px' }}>
          Debug: {JSON.stringify(props, null, 2)}
        </pre>
      </div>
    );
  }
  
  return (
    <div className="my-widget">
      <h2>My Widget</h2>
      <p>{props.myData}</p>
    </div>
  );
}
```

Create `widgets/my_widget/_app.jsx`:

```jsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import MyWidget from './index.jsx';

// Mount the component
const rootElement = document.getElementById('my_widget-root');
if (rootElement) {
  const root = createRoot(rootElement);
  root.render(<MyWidget />);
} else {
  console.error('Root element #my_widget-root not found!');
}
```

### 2. Create MCP Tool

Create `server/tools/my_widget_tool.py`:

```python
from config.base_widget import BaseWidget
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any


class MyWidgetInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    my_data: str = Field(..., alias="myData")


class MyWidgetTool(BaseWidget):
    identifier = "my-widget"
    title = "My Widget"
    input_schema = MyWidgetInput
    invoking = "Preparing widget..."
    invoked = "Widget ready!"
    
    widget_csp = {
        "connect_domains": [],
        "resource_domains": ["https://persistent.oaistatic.com"]
    }
    
    async def execute(self, input_data: MyWidgetInput) -> Dict[str, Any]:
        return {
            "myData": input_data.my_data
        }
```

### 3. Register Widget

Add your widget to `server/main.py`:

```python
from server.tools import PizzaMapTool, PizzaListTool, MyWidgetTool

tools = [
    PizzaMapTool(build_results["pizza_map"]),
    PizzaListTool(build_results["pizza_list"]),
    MyWidgetTool(build_results["my_widget"]),  # Add your widget
]
```

### 4. Build and Test

```bash
# Build widgets
npm run build

# Restart server
python server/main.py

# Test the widget
python test_widgets.py
```

## 🧪 Testing

### Test Widget Components

```bash
python test_widgets.py
```

Validates:
- Widget builds successfully
- Tools initialize correctly
- Embedded resources are structured properly
- HTML content is valid
- Tools can execute and return data

### Test MCP Server Responses

```bash
python test_final.py
```

Validates:
- Widget metadata is included in responses
- OpenAI-specific fields are present
- HTML is embedded correctly
- Tools are registered properly

### Test MCP Responses (Detailed)

```bash
python test_mcp_responses.py
```

Provides detailed inspection of:
- `list_tools` response
- `call_tool` response
- `list_resources` response
- `read_resource` response

## 🔧 How It Works

### 1. Build Process

The build process converts React components into standalone HTML bundles:

```mermaid
widgets/my_widget/index.jsx 
  → Build with Vite (React + ReactDOM)
  → assets/my_widget-{hash}.html
  → Embedded in MCP tool response
```

Key features:
- All code inlined (React, ReactDOM, your component)
- Single HTML file per widget
- Auto-mounting via `_app.jsx`
- Content-hashed filenames

### 2. Widget Data Flow

```mermaid
ChatGPT → MCP Server → Tool.execute()
  → Returns { structuredContent: {...} }
  → ChatGPT passes to window.openai.toolOutput
  → React component reads via useWidgetProps()
  → Component renders with data
```

### 3. MCP Server Architecture

The server uses **direct MCP handler registration** (not FastMCP's `@tool` decorator) to ensure widget metadata is properly included:

```python
# Direct handler registration
@server.list_tools()
async def list_tools_handler():
    return [Tool(..., _meta=widget.get_tool_meta())]

# Custom call_tool handler with widget metadata
async def call_tool_handler(req):
    result = await widget.execute(input_data)
    widget_resource = widget.get_embedded_resource()
    
    return ServerResult(
        CallToolResult(
            content=[TextContent(text=widget.invoked)],
            structuredContent=result,
            _meta={
                "openai.com/widget": widget_resource.model_dump(mode="json"),
                "openai/outputTemplate": widget.template_uri,
                "openai/widgetAccessible": True,
                "openai/resultCanProduceWidget": True,
            }
        )
    )
```

## 📝 Widget Configuration

### BaseWidget Properties

```python
class MyWidgetTool(BaseWidget):
    # Required
    identifier = "my-widget"           # Tool ID in MCP
    title = "My Widget"                # Display name
    input_schema = MyWidgetInput       # Pydantic input model
    
    # Optional
    description = "Widget description" # Tool description
    invoking = "Loading..."            # Message while executing
    invoked = "Done!"                  # Message when complete
    
    # OpenAI-specific options
    widget_accessible = True           # Enable widget display
    widget_description = None          # Widget hover text
    widget_prefers_border = False      # Show border in UI
    read_only = True                   # Widget is read-only
    
    # Content Security Policy
    widget_csp = {
        "connect_domains": [],         # Allowed fetch/XHR domains
        "resource_domains": []         # Allowed resource domains
    }
```

### Input Schema with Aliases

ChatGPT uses camelCase, but Python uses snake_case. Use aliases:

```python
class MyWidgetInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    # Python name: snake_case, ChatGPT name: camelCase
    pizza_topping: str = Field(..., alias="pizzaTopping")
    center_lat: float = Field(..., alias="centerLat")
    center_lng: float = Field(..., alias="centerLng")
```

## 🐛 Debugging

### Widget Not Displaying

1. **Check browser console** (F12 → Console):
   - Look for: `"MyWidget received props:"`
   - Look for: `"window.openai:"`

2. **Empty props `{}`**:
   - Server isn't returning `structuredContent`
   - Check tool's `execute()` method returns data

3. **Debug info shows data, but widget blank**:
   - Check component's render condition
   - Verify field names match (camelCase vs snake_case)

4. **Console errors about React**:
   - Check component has no syntax errors
   - Verify imports are correct

### Server Issues

```bash
# Check server is running
curl http://localhost:8001/

# Test tool directly
python test_final.py

# Check MCP responses
python test_mcp_responses.py
```

### Build Issues

```bash
# Clean build
rm -rf assets/*.html assets/*.js

# Rebuild
npm run build

# Check build output
ls -lh assets/
```

## 📚 Key Files

### `config/mcp_server.py`
Core MCP server that handles widget metadata. Uses direct handler registration to ensure OpenAI-specific metadata is included in responses.

### `config/base_widget.py`
Base class for all widgets. Provides methods for:
- `get_input_schema()` - JSON schema for tool inputs
- `get_tool_meta()` - OpenAI tool metadata
- `get_resource_meta()` - OpenAI resource metadata
- `get_embedded_resource()` - HTML resource for widget
- `execute()` - Tool execution logic (abstract method)

### `hooks/use-widget-props.ts`
React hook that reads `window.openai.toolOutput` to get data passed from ChatGPT.

### `build-all.mts`
Vite build script that:
1. Finds all widget entry points (`_app.jsx` or `index.jsx`)
2. Bundles with React + ReactDOM
3. Inlines everything into single HTML file
4. Content-hashes filenames
5. Generates mount script

## 🎯 Best Practices

1. **Always include debug output** during development
2. **Test locally** with `test_widgets.py` before deploying
3. **Use type hints** in Python and TypeScript
4. **Keep widgets simple** - complex logic should be in the tool
5. **Handle loading states** - data may arrive async
6. **Use camelCase aliases** for ChatGPT compatibility
7. **Validate inputs** with Pydantic models
8. **Add CSP domains** if your widget fetches external resources

## 📖 Examples

See the included widgets for reference:
- **pizza_list**: Simple list display
- **pizza_map**: More complex with styling

## 🤝 Contributing

To add new features:
1. Create feature branch
2. Add tests
3. Update documentation
4. Submit PR

## 📄 License

MIT

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review test output
- Check browser console
- Verify MCP responses with test scripts
