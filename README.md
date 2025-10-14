# ChatGPT Widget Framework

OpenAI Apps SDK 공식 스펙을 준수하는 ChatGPT 위젯 프레임워크입니다.

## 폴더 구조

프레임워크는 3개의 핵심 폴더로 구성됩니다:

```
framework/
├── config/          # 1. 설정/Boilerplate
│   ├── builder.py   # React 빌드 자동화
│   ├── base_widget.py  # BaseWidget 추상 클래스
│   ├── mcp_server.py   # MCP 서버 래퍼
│   └── handlers.py     # MCP 핸들러
│
├── server/          # 2. MCP 서버 & Tools
│   ├── main.py      # 서버 진입점
│   ├── api/         # 커스텀 API (비즈니스 로직)
│   └── tools/       # MCP Tools (widgets + api)
│
├── widgets/         # 3. React UI (순수 컴포넌트)
│   ├── pizza_map/
│   └── pizza_list/
│
├── hooks/           # React 공통 hooks
└── assets/          # 빌드 결과
```

## 요구 사항

- **Python 3.10 이상** (Python 3.11 권장)
- **Node.js 16 이상**

## 설치

### 1. Python 가상환경 생성

**중요:** 이 프로젝트는 Python 3.10 이상이 필요합니다. 먼저 Python 버전을 확인하세요:

```bash
python3.11 --version  # 또는 python3.10 --version
```

가상환경을 생성하고 활성화합니다:

```bash
cd flick
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
# venv\Scripts\activate  # Windows
```

활성화되면 터미널에 `(venv)`가 표시됩니다.

### 2. Python 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Node 의존성 설치

```bash
npm install
```

## 사용법

**참고:** 서버를 실행하기 전에 항상 가상환경을 활성화하세요:

```bash
source venv/bin/activate  # macOS/Linux
# 또는
# venv\Scripts\activate  # Windows
```

### 1. React 컴포넌트 빌드

```bash
npm run build
```

### 2. MCP 서버 실행

```bash
cd server
python main.py
```

서버는 `http://0.0.0.0:8001`에서 실행됩니다.

### 가상환경 비활성화

작업이 끝나면 가상환경을 비활성화할 수 있습니다:

```bash
deactivate
```

### MCP 엔드포인트:
- `GET /mcp` - SSE 엔드포인트
- `POST /mcp/messages` - 메시지 엔드포인트

## 새로운 위젯 추가하기

### 1. React 컴포넌트 생성

`widgets/my_widget/index.jsx`:
```jsx
import React from 'react';
import { useWidgetProps } from '../../hooks/use-widget-props';

export default function MyWidget() {
  const props = useWidgetProps();
  return <div>{props.data}</div>;
}
```

### 2. API 함수 작성 (선택사항)

`server/api/my_api.py`:
```python
async def get_my_data():
    return {"result": "data"}
```

### 3. MCP Tool 정의

`server/tools/my_tool.py`:
```python
from config.base_widget import BaseWidget
from pydantic import BaseModel
from ..api.my_api import get_my_data

class MyInput(BaseModel):
    query: str

class MyTool(BaseWidget):
    identifier = "my-widget"
    title = "My Widget"
    input_schema = MyInput
    
    async def execute(self, input_data: MyInput):
        data = await get_my_data()
        return {"data": data}
```

### 4. server/main.py에 등록

```python
from tools import MyTool

tools = [
    MyTool(build_results["my_widget"]),
    # ... 기존 tools
]
```

### 5. 빌드 및 실행

```bash
# 가상환경 활성화 (아직 활성화하지 않은 경우)
source venv/bin/activate

# React 빌드 및 서버 실행
npm run build
cd server && python main.py
```

## 고급 기능

### CSP (Content Security Policy) 설정

```python
class MyTool(BaseWidget):
    widget_csp = {
        "connect_domains": ["https://api.example.com"],
        "resource_domains": ["https://cdn.example.com"]
    }
```

### 위젯 설명 추가

```python
class MyTool(BaseWidget):
    widget_description = "Interactive UI for displaying data"
```

### Border 옵션

```python
class MyTool(BaseWidget):
    widget_prefers_border = True
```

## 문제 해결

### Python 버전 문제

만약 `pip install -r requirements.txt` 실행 시 Python 버전 에러가 발생한다면:

**macOS (Homebrew 사용):**
```bash
# Python 3.11 설치
brew install python@3.11

# 가상환경 재생성
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Conda 사용:**
```bash
# Python 3.11로 conda 환경 생성
conda create -n flick python=3.11 -y
conda activate flick
pip install -r requirements.txt
```

### 패키지 설치 오류

가상환경을 삭제하고 재생성하세요:
```bash
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 참고 문서

- [OpenAI Apps SDK - MCP Server](https://developers.openai.com/apps-sdk/build/mcp-server)
- [OpenAI Apps SDK - Custom UX](https://developers.openai.com/apps-sdk/build/custom-ux)

## 라이선스

MIT

