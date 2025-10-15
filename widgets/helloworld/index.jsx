import React from 'react';
import { useWidgetProps } from 'chatjs-hooks';

export default function HelloWorld() {
  const props = useWidgetProps();
  
  // Debug: log what we received
  React.useEffect(() => {
    console.log('HelloWorld received props:', props);
  }, [props]);
  
  return (
    <div className="helloworld" style={{
      padding: '20px',
      textAlign: 'center',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{
        fontSize: '48px',
        color: '#4A90E2',
        marginBottom: '20px',
        textShadow: '2px 2px 4px rgba(0,0,0,0.1)'
      }}>
        🌍 {props.message || 'Hello World!'} 🌍
      </h1>
      
      <p style={{
        fontSize: '18px',
        color: '#666',
        marginTop: '10px'
      }}>
        Welcome to your first Flick widget!
      </p>
      
      {props.timestamp && (
        <p style={{
          fontSize: '14px',
          color: '#999',
          marginTop: '15px'
        }}>
          Generated at: {props.timestamp}
        </p>
      )}
      
      <div style={{
        marginTop: '30px',
        padding: '15px',
        background: '#f5f5f5',
        borderRadius: '8px',
        fontSize: '12px',
        color: '#888'
      }}>
        <strong>Debug Info:</strong>
        <pre style={{ textAlign: 'left', marginTop: '10px' }}>
          {JSON.stringify(props, null, 2)}
        </pre>
      </div>
    </div>
  );
}

