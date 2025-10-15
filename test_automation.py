#!/usr/bin/env python3
"""
Flick Framework 자동화 테스트

이 스크립트는 자동화 기능들이 제대로 작동하는지 테스트합니다:
1. 위젯 파일 자동 생성
2. Tool 자동 발견 및 등록
"""

from pathlib import Path
import sys
import importlib
import inspect
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent))

from config.builder import WidgetBuilder
from config.base_widget import BaseWidget


def test_auto_generate_files():
    """
    위젯 발견 테스트
    
    더 이상 boilerplate 파일을 생성하지 않습니다!
    이제 mounting 로직은 빌드 시 자동으로 주입됩니다.
    """
    print("\n🧪 Testing Widget Discovery (No More Boilerplate!)...")
    print("=" * 60)
    
    PROJECT_ROOT = Path(__file__).parent
    
    # 테스트용 임시 위젯 생성
    test_widget_dir = PROJECT_ROOT / "widgets" / "test_temp"
    test_widget_dir.mkdir(exist_ok=True)
    
    try:
        # index.jsx만 생성
        index_file = test_widget_dir / "index.jsx"
        index_file.write_text("""
import React from 'react';
export default function TestTemp() {
  return <div>Test</div>;
}
""")
        
        print(f"\n✓ Created test widget at: {test_widget_dir}")
        print(f"  - index.jsx: ✓ (Only file needed!)")
        
        # 빌더 실행
        builder = WidgetBuilder(PROJECT_ROOT)
        builder._auto_generate_widget_files()
        
        # 확인: boilerplate 파일이 없어야 함
        app_file = test_widget_dir / "_app.jsx"
        pkg_file = test_widget_dir / "package.json"
        vite_file = test_widget_dir / "vite.config.mts"
        
        print(f"\n📦 Widget structure (simpler is better!):")
        print(f"  - _app.jsx: {'✗ (not needed!)' if not app_file.exists() else '✓ (should not exist)'}")
        print(f"  - package.json: {'✗ (not needed!)' if not pkg_file.exists() else '✓ (should not exist)'}")
        print(f"  - vite.config.mts: {'✗ (not needed!)' if not vite_file.exists() else '✓ (should not exist)'}")
        
        # 성공 조건: boilerplate 파일이 없어야 함!
        success = not any([app_file.exists(), pkg_file.exists(), vite_file.exists()])
        
        if success:
            print("\n✅ Widget discovery test PASSED!")
            print("   No boilerplate files needed - mounting logic is injected at build time!")
        else:
            print("\n❌ Widget discovery test FAILED!")
            print("   Unexpected boilerplate files found!")
        
        return success
        
    finally:
        # 정리
        if test_widget_dir.exists():
            shutil.rmtree(test_widget_dir)
            print(f"\n🧹 Cleaned up test widget")


def test_auto_load_tools():
    """Tool 자동 로드 테스트"""
    print("\n🧪 Testing Auto-Loading of Tools...")
    print("=" * 60)
    
    PROJECT_ROOT = Path(__file__).parent
    TOOLS_DIR = PROJECT_ROOT / "server" / "tools"
    
    # 모든 *_tool.py 파일 찾기
    tool_files = list(TOOLS_DIR.glob("*_tool.py"))
    print(f"\n📁 Found {len(tool_files)} tool files:")
    for tf in tool_files:
        print(f"   - {tf.name}")
    
    # 자동 로드 테스트
    loaded_tools = []
    for tool_file in tool_files:
        module_name = tool_file.stem
        try:
            module = importlib.import_module(f"server.tools.{module_name}")
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseWidget) and obj is not BaseWidget:
                    loaded_tools.append({
                        "name": name,
                        "identifier": obj.identifier,
                        "title": obj.title
                    })
                    print(f"\n✓ Loaded: {name}")
                    print(f"  - Identifier: {obj.identifier}")
                    print(f"  - Title: {obj.title}")
        except Exception as e:
            print(f"\n✗ Failed to load {tool_file.name}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   - Tool files found: {len(tool_files)}")
    print(f"   - Tools loaded: {len(loaded_tools)}")
    
    success = len(loaded_tools) > 0
    if success:
        print("\n✅ Auto-loading test PASSED!")
    else:
        print("\n❌ Auto-loading test FAILED!")
    
    return success


def test_full_integration():
    """전체 통합 테스트"""
    print("\n🧪 Testing Full Integration...")
    print("=" * 60)
    
    PROJECT_ROOT = Path(__file__).parent
    TOOLS_DIR = PROJECT_ROOT / "server" / "tools"
    
    try:
        # 1. 빌드
        print("\n📦 Step 1: Building widgets...")
        builder = WidgetBuilder(PROJECT_ROOT)
        build_results = builder.build_all()
        print(f"✓ Built {len(build_results)} widgets")
        
        # 2. Tool 자동 로드
        print("\n🔧 Step 2: Auto-loading tools...")
        tools = []
        for tool_file in TOOLS_DIR.glob("*_tool.py"):
            module_name = tool_file.stem
            try:
                module = importlib.import_module(f"server.tools.{module_name}")
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseWidget) and obj is not BaseWidget:
                        tool_identifier = obj.identifier
                        if tool_identifier in build_results:
                            tool_instance = obj(build_results[tool_identifier])
                            tools.append(tool_instance)
                            print(f"✓ Loaded: {name} ({tool_identifier})")
            except Exception as e:
                print(f"✗ Error: {tool_file.name}: {e}")
        
        # 3. 결과 검증
        print(f"\n📊 Integration Results:")
        print(f"   - Widgets built: {len(build_results)}")
        print(f"   - Tools loaded: {len(tools)}")
        print(f"   - Match rate: {len(tools)/len(build_results)*100:.0f}%")
        
        success = len(tools) > 0 and len(tools) == len([t for t in TOOLS_DIR.glob("*_tool.py")])
        if success:
            print("\n✅ Integration test PASSED!")
        else:
            print("\n❌ Integration test FAILED!")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Integration test FAILED with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 테스트 실행"""
    print("\n" + "=" * 60)
    print("🚀 Flick Framework Automation Tests")
    print("=" * 60)
    
    results = {
        "Widget Discovery": test_auto_generate_files(),
        "Auto-Loading": test_auto_load_tools(),
        "Full Integration": test_full_integration()
    }
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20s} {status}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests PASSED!")
    else:
        print("⚠️  Some tests FAILED!")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

