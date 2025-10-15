# Restart Your Server

Your widgets have been updated with debugging info. Follow these steps:

## 1. Stop the current server
Press `CTRL+C` in the terminal where the server is running

## 2. Restart the server
```bash
cd /Users/yunhyeok/Desktop/flick/flick
source venv/bin/activate
python server/main.py
```

## 3. Test in ChatGPT
Try calling one of your tools:
- "Show me pepperoni pizza places"
- "Find me pizza locations with mushrooms"

## What to Look For

### If it works:
You should see a list of pizza places with names, addresses, and ratings ⭐

### If you still see an empty box:
Open the browser console (F12 → Console) and look for:
- `PizzaList received props:` or `PizzaMap received props:`
- `window.openai:` 

This will show you what data ChatGPT is passing to your widget.

### Common Issues:

**Issue 1: Debug shows empty props `{}`**
- ChatGPT isn't passing `structuredContent` correctly
- Check that your MCP server is returning the data

**Issue 2: Debug shows the data**
- The hook is working but the render condition might be wrong
- Check if `pizzaTopping` field name matches

**Issue 3: Console errors about React**
- The component might have a rendering issue
- Check for any red errors in console

## Quick Test
You can also test the widget locally:
```bash
python test_final.py
```

This validates that your server is returning the correct metadata.

