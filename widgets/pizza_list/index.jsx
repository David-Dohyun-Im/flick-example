import React from 'react';
import { useWidgetProps } from '../../hooks/use-widget-props';

export default function PizzaList() {
  const props = useWidgetProps();
  
  return (
    <div className="pizza-list">
      <h2>{props.pizzaTopping} Pizza Places</h2>
      <ul>
        {props.places?.map((place, idx) => (
          <li key={idx}>
            {place.name} - {place.address}
          </li>
        ))}
      </ul>
    </div>
  );
}

