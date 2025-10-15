# Floydr Example Project

Example ChatGPT widget application built with the [Floydr Framework](https://pypi.org/project/floydr/).

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install floydr httpx

# Install Node packages
npm install
```

### 2. Build Widgets

```bash
npm run build
```

This will:
- Discover all widgets in `widgets/` directory
- Bundle them with React and inject mounting logic
- Generate optimized HTML files in `assets/`

### 3. Run the Server

```bash
python server/main.py
```

Server will start at: **http://0.0.0.0:8001**

## Project Structure

```
.
├── widgets/              # React widget components
│   ├── helloworld/
│   │   └── index.jsx    # Simple "Hello World" widget
│   ├── pizza_list/
│   │   └── index.jsx    # List view of pizza places
│   └── pizza_map/
│       └── index.jsx    # Map view of pizza places
│
├── server/
│   ├── tools/           # MCP widget tools (auto-discovered)
│   │   ├── helloworld_tool.py
│   │   ├── pizza_list_tool.py
│   │   └── pizza_map_tool.py
│   ├── api/
│   │   └── pizzeria_api.py  # External API integration
│   └── main.py          # Server entry point
│
├── assets/              # Built widget bundles (auto-generated)
├── package.json
└── requirements.txt
```

## Example Widgets

### 1. Hello World
**Identifier**: `helloworld`  
**Purpose**: Demonstrates basic Floydr usage

```python
from floydr import BaseWidget
```

```jsx
import { useWidgetProps } from 'floydr';
```

### 2. Pizza List
**Identifier**: `pizza_list`  
**Purpose**: Shows API integration and list rendering

**Input**: Pizza topping (e.g., "pepperoni")  
**Output**: List of pizza places with that topping

### 3. Pizza Map
**Identifier**: `pizza_map`  
**Purpose**: Demonstrates CSP configuration for external APIs

**Features**:
- External API calls (Mapbox)
- CSP configuration
- Border preference

## Floydr Commands

### Framework Import
```python
# In your tool files
from floydr import BaseWidget, Field, ConfigDict, WidgetMCPServer, WidgetBuilder
```

### React Hooks
```jsx
// In your widget components
import { useWidgetProps, useWidgetState, useOpenAiGlobal } from 'floydr';
```

### Build Commands
```bash
# Build all widgets
npm run build

# The build script is provided by floydr:
# node_modules/floydr/build-all.mts
```

### Python Commands
```bash
# Start development server
python server/main.py

# Create a new widget (with templates!)
python -m floydr.cli.main create mywidget

# Run tests
python test_widgets.py
python test_final.py

# Check floydr installation
pip show floydr

# Upgrade floydr
pip install --upgrade floydr
```

### NPM Commands
```bash
# Install dependencies
npm install

# Build widgets
npm run build

# Check floydr version
npm list floydr

# Upgrade floydr
npm install floydr@latest
```

## Creating a New Widget

### Quick Method: Use Floydr CLI ⚡

```bash
# Automatically generates both files with templates!
python -m floydr.cli.main create mywidget

# Or if floydr command is available:
floydr create mywidget
```

This creates:
- `server/tools/mywidget_tool.py` (with template)
- `widgets/mywidget/index.jsx` (black bg, white text template)

Then just:
```bash
npm run build
python server/main.py
```

**That's it!** Widget is automatically discovered and registered.

---

### Manual Method (Optional)

If you prefer to create files manually:

#### Step 1: Create Tool File

Create `server/tools/mywidget_tool.py`:

```python
from floydr import BaseWidget, ConfigDict
from pydantic import BaseModel
from typing import Dict, Any

class MywidgetInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    # Add your input fields here

class MywidgetTool(BaseWidget):
    identifier = "mywidget"  # Must match folder name
    title = "My Widget"
    input_schema = MywidgetInput
    invoking = "Loading widget..."
    invoked = "Widget ready!"
    
    widget_csp = {
        "connect_domains": [],
        "resource_domains": []
    }
    
    async def execute(self, input_data: MywidgetInput) -> Dict[str, Any]:
        # Your logic here
        return {
            "message": "Hello from My Widget"
        }
```

### Step 2: Create React Component

Create `widgets/mywidget/index.jsx`:

```jsx
import React from 'react';
import { useWidgetProps } from 'flicky-react';

export default function Mywidget() {
  const props = useWidgetProps();
  
  return (
    <div style={{
      background: '#000',
      color: '#fff',
      padding: '40px',
      textAlign: 'center',
      borderRadius: '8px',
      fontFamily: 'monospace'
    }}>
      <h1>{props.message || 'Welcome to Floydr'}</h1>
    </div>
  );
}
```

#### Step 3: Build and Run

```bash
# Build widgets
npm run build

# Restart server  
python server/main.py
```

**That's it!** Your widget is automatically discovered and registered.

## Development Workflow

```bash
# 1. Make changes to widget or tool
vim widgets/mywidget/index.jsx
vim server/tools/mywidget_tool.py

# 2. Rebuild
npm run build

# 3. Restart server
# Stop: Ctrl+C
python server/main.py

# 4. Test in ChatGPT
# Connect to: http://localhost:8001
```

## Testing

```bash
# Test widget builds
python test_widgets.py

# Test MCP server
python test_final.py

# Test MCP responses (detailed)
python test_mcp_responses.py
```

## Configuration

### Widget CSP (Content Security Policy)

For widgets that need external resources:

```python
class MyTool(BaseWidget):
    widget_csp = {
        "connect_domains": ["https://api.example.com"],
        "resource_domains": ["https://cdn.example.com"]
    }
```

### Widget Options

```python
class MyTool(BaseWidget):
    widget_accessible = True
    widget_prefers_border = False
    read_only = True
    widget_description = "Optional description"
```

## Common Commands Reference

### Installation & Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install flicky httpx
npm install
```

### Development
```bash
npm run build                    # Build widgets
python server/main.py            # Start server
python test_widgets.py           # Run tests
```

### Maintenance
```bash
pip list | grep flicky            # Check version
pip install --upgrade flicky      # Upgrade framework
npm install flicky-react@latest   # Upgrade React package
```

### Debugging
```bash
# Check if flicky is installed
python -c "import flicky; print(flicky.__version__)"

# Check widget discovery
python -c "from pathlib import Path; from flicky import WidgetBuilder; b = WidgetBuilder(Path('.')); print(list(b.widgets_dir.iterdir()))"

# List built assets
ls -lh assets/
```

## Troubleshooting

### Module Not Found: floydr
```bash
pip install floydr
# Make sure venv is activated
```

### Module Not Found: floydr (npm)
```bash
npm install floydr
# Check node_modules/floydr exists
```

### Build Fails
```bash
# Make sure floydr provides build-all.mts
ls node_modules/floydr/build-all.mts

# Reinstall if needed
npm install floydr --force
```

### Widgets Not Loading
- Ensure `identifier` in tool matches folder name
- Check widget has `index.jsx` with default export
- Rebuild: `npm run build`

## Learn More

- **Floydr (Python)**: https://pypi.org/project/floydr/
- **Floydr (npm)**: https://www.npmjs.com/package/floydr
- **MCP Specification**: https://modelcontextprotocol.io/

## License

MIT
