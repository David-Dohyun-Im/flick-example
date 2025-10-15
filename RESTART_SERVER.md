# Quick Restart Guide

Your widgets have been updated. Follow these steps to restart and test.

## 🔄 Restart Server

### 1. Stop Current Server
Press `CTRL+C` in the terminal running the server

### 2. Restart Server
```bash
cd /Users/yunhyeok/Desktop/flick/flick
source venv/bin/activate
python server/main.py
```

The server will:
- ✅ Build widgets automatically on startup
- ✅ Load React components from `assets/` directory
- ✅ Start MCP server on `http://0.0.0.0:8001`

### 3. Verify Server is Running
You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
```

## 🧪 Quick Test

Before testing in ChatGPT, validate locally:

```bash
# Test that widgets built correctly
python test_widgets.py

# Test that MCP server returns proper metadata
python test_final.py
```

Both tests should show:
```
✅ ALL TESTS PASSED!
```

## 🎯 Test in ChatGPT

### Try These Commands:

1. **Pizza List**
   ```
   Show me pepperoni pizza places
   ```

2. **Pizza Map**
   ```
   Find pizza locations with margherita
   ```

## 🔍 What to Look For

### ✅ Success - You Should See:

**Pizza List Widget:**
- A list of pizza places
- Restaurant names in bold
- Addresses next to names
- Star ratings (⭐) if available

**Pizza Map Widget:**
- Title with topping name
- Cards for each location
- Restaurant names, addresses
- Star ratings in styled cards

### ❌ Issue - Empty Box

If you see an empty box, the component loaded but has no data.

**Open Browser Console** (Press F12 → Console Tab)

Look for these debug messages:
```javascript
PizzaList received props: {pizzaTopping: "pepperoni", places: [...]}
window.openai: {toolOutput: {...}}
```

### 🐛 Debug Scenarios

**Scenario 1: Empty Props `{}`**
```
Debug: {}
```
**Problem:** Server isn't passing data  
**Fix:** Check your tool's `execute()` method returns the right structure

---

**Scenario 2: Shows "Loading pizza places..."**
```
Loading pizza places...
Waiting for data...
Debug: {}
```
**Problem:** `pizzaTopping` field is missing  
**Fix:** Check the field name matches between tool and component (camelCase vs snake_case)

---

**Scenario 3: Props Look Correct, But Widget Empty**
```javascript
// Console shows:
PizzaList received props: {pizzaTopping: "pepperoni", places: []}
```
**Problem:** API returned empty array  
**Fix:** Check `pizzeria_api.py` is returning data

---

**Scenario 4: Console Errors**
```javascript
Error: Cannot read property 'map' of undefined
```
**Problem:** Component trying to render before data loads  
**Fix:** Already handled with loading states in updated components

## 🔧 Common Fixes

### Widget Changes Not Showing

```bash
# Force rebuild
cd /Users/yunhyeok/Desktop/flick/flick
rm -rf assets/*.html
npm run build
python server/main.py
```

### Server Won't Start

```bash
# Check if port is in use
lsof -i :8001

# Kill existing process
kill -9 <PID>

# Restart
python server/main.py
```

### Python Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastmcp
```

## 📊 Validation Checklist

Before marking as complete:

- [ ] Server starts without errors
- [ ] `test_widgets.py` passes
- [ ] `test_final.py` passes
- [ ] Widget displays in ChatGPT
- [ ] Data appears in widget
- [ ] Console shows no errors

## 📝 Next Steps

Once everything works:

1. **Remove debug code** from components (optional)
2. **Add styling** to make widgets prettier
3. **Create more widgets** using the same pattern
4. **Read the full README.md** for advanced features

## 🆘 Still Not Working?

1. Check all files were saved
2. Verify virtual environment is activated
3. Look at server logs for errors
4. Check ChatGPT gave the server the correct URL
5. Try a different widget to isolate the issue

---

**Need more help?** See the full documentation in `README.md`
