
export function handleUploadImage(data, envData) {

    //data.append('file', this.uploadInput.files[0]);
    //data.append('filename', this.fileName.value);

    fetch(`${envData.API_URL}upload`, {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ imageURL: `${envData.API_URL}${body.file}` });
      });
    });
  }