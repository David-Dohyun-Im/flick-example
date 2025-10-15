import React from 'react';
import { createRoot } from 'react-dom/client';
import PizzaList from './index.jsx';

// Mount the component when the script loads
const rootElement = document.getElementById('pizza_list-root');
if (rootElement) {
  const root = createRoot(rootElement);
  root.render(<PizzaList />);
} else {
  console.error('Root element #pizza_list-root not found!');
}

