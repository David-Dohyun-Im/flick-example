import React from 'react';
import { createRoot } from 'react-dom/client';
import PizzaMap from './index.jsx';

// Mount the component when the script loads
const rootElement = document.getElementById('pizza_map-root');
if (rootElement) {
  const root = createRoot(rootElement);
  root.render(<PizzaMap />);
} else {
  console.error('Root element #pizza_map-root not found!');
}

