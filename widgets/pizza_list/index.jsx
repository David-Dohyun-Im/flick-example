import React from 'react';
import { useWidgetProps } from 'floydr';

export default function PizzaList() {
  const props = useWidgetProps();
  
  // Debug: log what we received
  React.useEffect(() => {
    console.log('PizzaList received props:', props);
    console.log('window.openai:', window.openai);
  }, [props]);
  
  // If no data yet, show loading/waiting state
  if (!props.pizzaTopping) {
    return (
      <div className="pizza-list">
        <h2>Loading pizza places...</h2>
        <p>Waiting for data...</p>
        <pre style={{ fontSize: '10px', background: '#f5f5f5', padding: '10px' }}>
          Debug: {JSON.stringify(props, null, 2)}
        </pre>
      </div>
    );
  }
  
  return (
    <div className="pizza-list">
      <h2>{props.pizzaTopping} Pizza Places</h2>
      {!props.places || props.places.length === 0 ? (
        <p>No places found</p>
      ) : (
        <ul>
          {props.places.map((place, idx) => (
            <li key={idx}>
              <strong>{place.name}</strong> - {place.address}
              {place.rating && <span> ⭐ {place.rating}</span>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

