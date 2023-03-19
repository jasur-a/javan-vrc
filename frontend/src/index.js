import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import EnvProvider from './EnvContext';
import './index.css';

console.log("::process", process.env )
const envData = Object.keys(process.env)
const container = document.getElementById('root');
const root = createRoot(container); 

root.render(
    <EnvProvider envData={envData}>
        <App />
    </EnvProvider>
);