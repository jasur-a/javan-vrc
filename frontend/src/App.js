import React from 'react';
import Main from './components/Main/Main'
import './App.css';

const App = (envData) => (
    <section className='App'>
      <h1 className='App-title'>Converter Video to Text</h1>
      <p>Agregar una breve descripcion aqui</p>
      <Main envData={envData} />
    </section>
);

export default App;