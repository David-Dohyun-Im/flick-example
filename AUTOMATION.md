# 🚀 Flick Framework Automation

Flick Framework는 위젯 개발을 최대한 간단하게 만들기 위해 많은 부분을 자동화했습니다.

## ✨ 자동화된 기능들

### 1. Mounting 로직 자동 주입 (No More Boilerplate!)

더 이상 **어떤 boilerplate 파일도 필요하지 않습니다!**

**이전 방식:**
```bash
# 각 위젯마다 수동으로 생성해야 했던 파일들
widgets/my_widget/
├── index.jsx           # 수동 생성
├── _app.jsx            # 수동 생성 (boilerplate)
├── package.json        # 수동 생성 (거의 동일한 내용)
└── vite.config.mts     # 수동 생성 (거의 동일한 내용)
```

**새로운 방식:**
```bash
# 이제 index.jsx만 만들면 됩니다!
widgets/my_widget/
└── index.jsx           # 이것만 만들면 끝!

# mounting 로직은 빌드 시 자동으로 주입됩니다 ✨
```

#### 구현 위치
`build-all.mts`의 `wrapEntryPlugin()` 함수

```typescript
function wrapEntryPlugin(virtualId: string, entryFile: string, widgetName: string): Plugin {
  return {
    load(id) {
      // 빌드 시 mounting 로직을 자동으로 주입!
      return `
        import React from 'react';
        import { createRoot } from 'react-dom/client';
        import Component from ${JSON.stringify(entryFile)};

        // Auto-mount the component
        const rootElement = document.getElementById('${widgetName}-root');
        if (rootElement) {
          const root = createRoot(rootElement);
          root.render(React.createElement(Component));
        }
      `;
    },
  };
}
```

### 2. Tool 자동 발견 및 등록

더 이상 `__init__.py`와 `main.py`를 수동으로 업데이트할 필요가 없습니다!

**이전 방식:**
```python
# server/tools/__init__.py - 매번 수동 업데이트 필요
from .pizza_map_tool import PizzaMapTool
from .pizza_list_tool import PizzaListTool
from .my_new_tool import MyNewTool  # 추가해야 함
__all__ = ["PizzaMapTool", "PizzaListTool", "MyNewTool"]  # 추가해야 함

# server/main.py - 매번 수동 업데이트 필요
from server.tools import PizzaMapTool, PizzaListTool, MyNewTool

tools = [
    PizzaMapTool(build_results["pizza_map"]),
    PizzaListTool(build_results["pizza_list"]),
    MyNewTool(build_results["my_new"]),  # 추가해야 함
]
```

**새로운 방식:**
```python
# server/tools/__init__.py - 더 이상 수정 불필요!
"""
MCP Tools - BaseWidget을 상속받아 구현된 도구들

✨ 이 파일은 더 이상 수동으로 관리하지 않아도 됩니다!
"""

# server/main.py - 자동으로 모든 tool 발견!
def auto_load_tools(build_results):
    """tools 디렉토리에서 자동으로 Tool 클래스들을 로드"""
    tools = []
    
    # *_tool.py 파일들을 자동 스캔
    for tool_file in TOOLS_DIR.glob("*_tool.py"):
        module_name = tool_file.stem
        module = importlib.import_module(f"server.tools.{module_name}")
        
        # BaseWidget을 상속받은 클래스 자동 발견
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseWidget) and obj is not BaseWidget:
                tool_identifier = obj.identifier
                if tool_identifier in build_results:
                    tool_instance = obj(build_results[tool_identifier])
                    tools.append(tool_instance)
    
    return tools
```

#### 구현 위치
`server/main.py`의 `auto_load_tools()` 함수

## 🎯 새로운 위젯 추가하기 (완전 자동화)

### Before (7 Steps) ❌
1. `widgets/my_widget/index.jsx` 생성
2. `widgets/my_widget/_app.jsx` 생성 (boilerplate)
3. `widgets/my_widget/package.json` 생성 (boilerplate)
4. `widgets/my_widget/vite.config.mts` 생성 (boilerplate)
5. `server/tools/my_widget_tool.py` 생성
6. `server/tools/__init__.py` 업데이트 (import 추가)
7. `server/main.py` 업데이트 (tool 등록)

### After (2 Steps) ✅
1. `widgets/my_widget/index.jsx` 생성
2. `server/tools/my_widget_tool.py` 생성

**끝!** 🎉

각 위젯 디렉토리는 이제 단 하나의 파일만 포함합니다:

```
widgets/
  my_widget/
    └── index.jsx  ← 이것만!
  another_widget/
    └── index.jsx  ← 이것만!
```

## 📋 체크리스트

새로운 위젯을 추가할 때:

- [ ] `server/tools/your_tool.py` 생성
  - `identifier`를 위젯 폴더명과 동일하게 설정 (snake_case)
  - `BaseWidget` 상속
  
- [ ] `widgets/your_widget/index.jsx` 생성
  - `useWidgetProps()` 훅 사용
  - default export로 컴포넌트 내보내기

- [ ] 서버 시작: `python server/main.py`
  - 자동으로 빌드 ✅
  - 자동으로 등록 ✅
  - 자동으로 서빙 ✅

## 🔍 디버깅

서버 시작 시 자동화 프로세스의 로그를 확인할 수 있습니다:

```bash
$ python server/main.py

✓ Auto-generated: widgets/my_widget/_app.jsx
✓ Auto-generated: widgets/my_widget/package.json
✓ Auto-generated: widgets/my_widget/vite.config.mts

✓ Loaded tool: MyWidgetTool (identifier: my_widget)
✓ Loaded tool: PizzaListTool (identifier: pizza_list)
✓ Loaded tool: PizzaMapTool (identifier: pizza_map)

🚀 Starting server with 3 tools
```

### 자주 발생하는 문제

1. **Tool이 로드되지 않음**
   - `identifier`가 위젯 폴더명과 일치하는지 확인
   - 파일명이 `*_tool.py` 형식인지 확인
   - `BaseWidget`을 상속받았는지 확인

2. **빌드 실패**
   - `widgets/your_widget/index.jsx`가 존재하는지 확인
   - default export가 있는지 확인
   - React 컴포넌트 문법 오류 확인

3. **위젯이 화면에 표시되지 않음**
   - 컴포넌트가 `export default`로 내보내지는지 확인
   - 빌드 로그에서 mounting 오류 확인
   - 브라우저 콘솔에서 `#widget-name-root not found` 오류 확인

## 🎨 커스터마이징

mounting 로직은 빌드 시스템에 통합되어 있습니다. 특별한 mounting 동작이 필요한 경우:

1. **Option 1**: `index.jsx` 컴포넌트 내에서 React hooks로 처리
   ```jsx
   export default function MyWidget() {
     useEffect(() => {
       // Custom initialization logic
     }, []);
   }
   ```

2. **Option 2**: `build-all.mts`의 `wrapEntryPlugin`을 프로젝트에 맞게 수정

대부분의 경우 기본 mounting 로직으로 충분합니다!

## 💡 Best Practices

1. **Naming Convention**
   - Tool 파일: `my_widget_tool.py` (snake_case, `_tool` suffix)
   - Widget 폴더: `my_widget/` (snake_case)
   - Identifier: `"my_widget"` (snake_case, 폴더명과 동일)
   - 컴포넌트: `MyWidget` (PascalCase)

2. **File Structure**
   ```
   server/tools/
   └── my_widget_tool.py     # Tool 클래스
   
   widgets/my_widget/
   └── index.jsx             # 이것만! Super simple!
   ```
   
   Mounting 로직, 빌드 설정 등은 모두 빌드 시스템에 통합되어 있습니다.

3. **Testing**
   - 새 위젯 추가 후 항상 서버 로그 확인
   - `✓ Auto-generated` 메시지 확인
   - `✓ Loaded tool` 메시지 확인

## 🚀 Next Steps

프레임워크를 더 개선하려면:

1. **Hot Reload**: 파일 변경 시 자동 재빌드
2. **Type Generation**: TypeScript 타입 자동 생성
3. **Template System**: 다양한 위젯 템플릿 제공
4. **CLI Tool**: `flick create my-widget` 같은 CLI 명령어
5. **Dev Server**: 개발용 실시간 프리뷰 서버


