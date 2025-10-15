# Flick - Quickstart Guide

Get your ChatGPT widgets running in 5 minutes.

## ⚡ Setup (First Time Only)

```bash
# Navigate to project
cd /Users/yunhyeok/Desktop/flick/flick

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
npm install

# Done! ✅
```

## 🚀 Run Server

```bash
# Activate virtual environment
cd /Users/yunhyeok/Desktop/flick/flick
source venv/bin/activate

# Start server (builds widgets automatically)
python server/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
```

## ✅ Test Locally

```bash
# In a new terminal (keep server running)
cd /Users/yunhyeok/Desktop/flick/flick
source venv/bin/activate

# Run tests
python test_final.py
```

Expected output:
```
✅ ALL TESTS PASSED!
Your widgets are ready to be served!
```

## 🎯 Use in ChatGPT

### 1. Configure MCP Server in ChatGPT

Add to your ChatGPT settings:
```json
{
  "mcpServers": {
    "flick": {
      "url": "http://localhost:8001/mcp"
    }
  }
}
```

### 2. Test Your Widgets

Try these commands:
- "Show me pepperoni pizza places"
- "Find margherita pizza locations"

You should see interactive widgets with restaurant data!

## 🛠️ Create Your First Widget

### 1. Create Component

`widgets/hello/index.jsx`:
```jsx
import React from 'react';
import { useWidgetProps } from '../../hooks/use-widget-props';

export default function Hello() {
  const props = useWidgetProps();
  
  if (!props.name) {
    return <div>Loading...</div>;
  }
  
  return <h1>Hello, {props.name}! 👋</h1>;
}
```

`widgets/hello/_app.jsx`:
```jsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import Hello from './index.jsx';

const root = document.getElementById('hello-root');
if (root) {
  createRoot(root).render(<Hello />);
}
```

### 2. Create Tool

`server/tools/hello_tool.py`:
```python
from config.base_widget import BaseWidget
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any


class HelloInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str


class HelloTool(BaseWidget):
    identifier = "hello"
    title = "Say Hello"
    input_schema = HelloInput
    invoking = "Saying hello..."
    invoked = "Hello sent!"
    
    async def execute(self, input_data: HelloInput) -> Dict[str, Any]:
        return {"name": input_data.name}
```

### 3. Register Tool

In `server/main.py`:
```python
from server.tools import PizzaMapTool, PizzaListTool
from server.tools.hello_tool import HelloTool  # Add this

tools = [
    PizzaMapTool(build_results["pizza_map"]),
    PizzaListTool(build_results["pizza_list"]),
    HelloTool(build_results["hello"]),  # Add this
]
```

### 4. Build & Test

```bash
# Build
npm run build

# Restart server
python server/main.py

# Test
python test_widgets.py
```

### 5. Use in ChatGPT

"Say hello to Alice"

You should see: **Hello, Alice! 👋**

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Restart Guide**: See `RESTART_SERVER.md`
- **Example Widgets**: Check `widgets/pizza_list/` and `widgets/pizza_map/`

## 🐛 Something Wrong?

### Widget not showing?
```bash
# Check browser console (F12)
# Look for: "received props" messages
```

### Build failed?
```bash
# Clean and rebuild
rm -rf assets/*.html
npm run build
```

### Server won't start?
```bash
# Check if port is in use
lsof -i :8001
# Kill if needed: kill -9 <PID>
```

### Tests failing?
```bash
# Reinstall dependencies
pip install -r requirements.txt
npm install
```

## 🎉 Next Steps

1. ✅ Server running
2. ✅ Tests passing
3. ✅ Widget displays in ChatGPT
4. → **Add more widgets!**
5. → **Customize styling**
6. → **Deploy to production**

Happy building! 🚀

