import React from 'react';
import { useWidgetProps } from 'chatjs-hooks';

export default function PizzaMap() {
  const props = useWidgetProps();
  
  // Debug: log what we received
  React.useEffect(() => {
    console.log('PizzaMap received props:', props);
    console.log('window.openai:', window.openai);
  }, [props]);
  
  // If no data yet, show loading/waiting state
  if (!props.pizzaTopping) {
    return (
      <div className="pizza-map">
        <h2>Loading pizza map...</h2>
        <p>Waiting for data...</p>
        <pre style={{ fontSize: '10px', background: '#f5f5f5', padding: '10px' }}>
          Debug: {JSON.stringify(props, null, 2)}
        </pre>
      </div>
    );
  }
  
  return (
    <div className="pizza-map">
      <h2>{props.pizzaTopping} Pizza Locations</h2>
      {!props.places || props.places.length === 0 ? (
        <p>No locations found</p>
      ) : (
        <div className="places-list">
          {props.places.map((place, idx) => (
            <div key={idx} className="place-item" style={{ 
              border: '1px solid #ddd', 
              padding: '10px', 
              marginBottom: '10px',
              borderRadius: '4px'
            }}>
              <h3 style={{ margin: '0 0 5px 0' }}>{place.name}</h3>
              <p style={{ margin: '0', color: '#666' }}>{place.address}</p>
              {place.rating && <p style={{ margin: '5px 0 0 0' }}>⭐ {place.rating}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

