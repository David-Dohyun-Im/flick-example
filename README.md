# Flick Example Project

This is an example project demonstrating the Flick framework for building ChatGPT widgets.

## Setup

This example uses the local Flick framework packages. Install them first:

### 1. Install Python Framework (Local)

```bash
cd /Users/yunhyeok/Desktop/flick/flick-pip
pip install -e .
```

### 2. Install React Hooks (Local)

```bash
cd /Users/yunhyeok/Desktop/flick/flick-npm
npm install
npm run build
npm link

cd /Users/yunhyeok/Desktop/flick/example
npm link flick-react
```

### 3. Install Project Dependencies

```bash
cd /Users/yunhyeok/Desktop/flick/example
pip install -r requirements.txt
npm install
```

## Running the Example

```bash
# Build widgets
npm run build

# Start the MCP server
python server/main.py

# Server runs at http://0.0.0.0:8001
```

## Example Widgets

This project includes three example widgets:

### 1. Hello World (`helloworld`)
A simple demonstration widget showing basic Flick usage.

```python
# server/tools/helloworld_tool.py
from flick import BaseWidget, ConfigDict
```

```jsx
// widgets/helloworld/index.jsx
import { useWidgetProps } from 'flick-react';
```

### 2. Pizza List (`pizza_list`)
Shows a list of pizza places based on topping preference.

### 3. Pizza Map (`pizza_map`)
Displays pizza places on a map with CSP configuration example.

## Framework Features Demonstrated

1. **Zero Boilerplate**: Each widget has only one file (`index.jsx`)
2. **Auto-Discovery**: Tools are automatically discovered from `server/tools/*_tool.py`
3. **Framework Imports**: Using `from flick import ...` and `from 'flick-react'`
4. **Auto-Build**: Mounting logic injected automatically during build

## Project Structure

```
example/
├── widgets/                 # React widget components
│   ├── helloworld/
│   │   └── index.jsx       # Only one file needed!
│   ├── pizza_list/
│   │   └── index.jsx
│   └── pizza_map/
│       └── index.jsx
│
├── server/                  # Python MCP server
│   ├── tools/              # Widget tools (auto-discovered)
│   │   ├── helloworld_tool.py
│   │   ├── pizza_list_tool.py
│   │   └── pizza_map_tool.py
│   ├── api/
│   │   └── pizzeria_api.py
│   └── main.py             # Clean server setup with Flick
│
├── assets/                  # Built widget bundles (auto-generated)
├── build-all.mts           # Build configuration
└── package.json
```

## Comparison: Before vs After Flick

### Before (Project Template)
```python
from config.base_widget import BaseWidget  # Internal path
from config.mcp_server import WidgetMCPServer
from config.builder import WidgetBuilder
```

### After (Flick Framework)
```python
from flick import BaseWidget, WidgetMCPServer, WidgetBuilder  # Clean API!
```

### React Components

Before:
```jsx
import { useWidgetProps } from '../../hooks/use-widget-props';  // Relative path
```

After:
```jsx
import { useWidgetProps } from 'flick-react';  // NPM package!
```

## Testing

```bash
# Run automated tests
python test_automation.py

# Test individual widgets
python test_widgets.py

# Test MCP responses
python test_final.py
```

## Learn More

- [Flick Framework Documentation](https://flick.dev/docs)
- [Flick Python API](https://flick.dev/docs/python)
- [Flick React Hooks](https://flick.dev/docs/react)
- [Creating Widgets Guide](https://flick.dev/docs/guides/creating-widgets)
