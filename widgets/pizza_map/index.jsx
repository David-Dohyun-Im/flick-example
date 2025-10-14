import React from 'react';
import { useWidgetProps } from '../../hooks/use-widget-props';

export default function PizzaMap() {
  const props = useWidgetProps();
  
  return (
    <div className="pizza-map">
      <h2>{props.pizzaTopping} Pizza Locations</h2>
      <div className="places-list">
        {props.places?.map((place, idx) => (
          <div key={idx} className="place-item">
            <h3>{place.name}</h3>
            <p>{place.address}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

