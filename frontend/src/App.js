import React from 'react';
import Main from './components/Main/Main'
import './App.css';

const App = (props) => {
    return (
    <section className='App'>
      <div className='header'>
        <h1 className='App-title'>Extracción de recetas de Videos</h1>
        <p>Para extraer una receta desde un video es necesario qu proporcione una URL o suba un archivo de video</p>
        <p>Este proceso puede demorar varios minutos hasta devolverle el documento descargable, por favor espere.</p>
      </div>
      <Main />
    </section>
)};

export default App;