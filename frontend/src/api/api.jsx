
import { saveAs } from 'file-saver';

const REACT_APP = /^REACT_APP_/i;

const envData = Object.keys(process.env)
// look for a REACT_APP
.filter((key) => REACT_APP.test(key))
// Integrate to array the key  of process.env with REACT_APP, start with empty object
.reduce((env, key) => {
  env[key] = process.env[key];
  return env;
}, {});


const generate_file = (data) => {

    const contentType = data.type;

    const fileContent = atob(data.file);
    const byteNumbers = new Array(fileContent.length);
    
    for (let i = 0; i < fileContent.length; i++) {
      byteNumbers[i] = fileContent.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: contentType });
    return blob
}

export async function generate_recipe(data) {

    //data.append('file', this.uploadInput.files[0]);
    //data.append('filename', this.fileName.value);
    fetch(`${envData.REACT_APP_API}upload`, {
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(data),
    }).then(response => response.json())
    .then(data => {
      if( data?.error){
        return data?.error
      }
      const fileName = data.name;
      // Guardar el archivo en el sistema de archivos local
      const blob = generate_file(data);
      saveAs(blob, fileName);
    })
    .catch(error => {
      console.error('Error al descargar el archivo:', error);
    });
  }

export async function get_recipes() {

    fetch(`${envData.REACT_APP_API}list`, {
      method: 'GET',
      headers: new Headers({
        "Content-Type": "application/json",
      }),
    }).then((response) => {
      response.json().then((body) => {
        console.log("::body", body)
        return body
      });
    }).catch(error => {
      console.error('Error:', error);
    });
  }

export async function download_recipe(data) {

    fetch(`${envData.REACT_APP_API}download-file`, {
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(data),
    }).then(response => response.blob())
    .then(blob => {
      // Guardar el archivo en el sistema de archivos local
      saveAs(blob, 'receta_chiles_poblanos.pdf');
      console.log("::bb", blob)
      //saveAs(blob, 'receta_chiles_poblanos.txt');
    })
    .catch(error => {
      console.error('Error al descargar el archivo:', error);
    });
  }