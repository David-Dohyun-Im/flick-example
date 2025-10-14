import { useState, useEffect } from 'react';

export function useWidgetProps<T = any>(): T {
  const [props, setProps] = useState<T>({} as T);
  
  useEffect(() => {
    // 공식 스펙: window.openai.toolOutput 사용
    if (window.openai?.toolOutput) {
      setProps(window.openai.toolOutput);
    }
  }, []);
  
  return props;
}

