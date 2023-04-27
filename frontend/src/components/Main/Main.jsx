import React from 'react';
import { modalLegals } from '../constants/constants';
import ModalWrapper from '../core/modalWrapper/ModalWrapper';
import { UploadVideo } from '../core/uploadVideo';
import { MainController } from './MainController';
import {  ContainerForm, Container, Form, Input, Label, Button, Header } from './Main.style';

export function Main (props) {

  const {
    handleChangeForm,
    handleSubmit,
    showModal, setShoModal,
    formData, setFormData,
    disabled
  } = MainController(props)

  return (
    <>
      <Container>
      <ModalWrapper modal={modalLegals} show={showModal}  handleShowModal={setShoModal} />
      
        <Header>
          <h1 className='App-title'>Extracción de recetas de Videos</h1>
          <p>Para extraer una receta desde un video es necesario que proporcione una URL o suba un archivo de video.</p>
          <p>Este proceso puede demorar varios minutos hasta devolverle el documento descargable. Por favor espere.</p>
        </Header> 

        <ContainerForm>
          <h3>Por favor indique el origen de su video</h3>
          <Form onSubmit={handleSubmit} onChange={handleChangeForm }>
            <div>
              <Label htmlFor="url">Por url (indique la url de youtube)</Label>
              <Input type="text"  name="url" disabled={disabled.url} required/>

            </div>
            <div>
              <Label htmlFor="fileUpload">Subir desde el ordenador </Label>
              
              <UploadVideo name="fileUpload" disabled={disabled.fileUpload} form={formData} formState={setFormData} required/>

            </div>

            <div>
              <Label htmlFor="legals"> <Input type="checkbox" className="checkbox" name="legals"  id="legals" disabled={disabled.fileUpload} required /> Acepto las <button type="button" className="link" onClick={() => setShoModal(true)}>políticas de uso </button> </Label>
            </div>

            <div>
              <Label htmlFor="is_mexican"> <Input type="checkbox" className="checkbox" name="is_mexican" id="is_mexican" />La receta ingresada es de comida Mexicana  </Label>
            </div>

            <div>
              Descargar en formato:
              <Label htmlFor="formatPDF"><Input type="radio" name="type_file" id="formatPDF" value="pdf" required />PDF</Label>
              <Label htmlFor="formatTXT"><Input type="radio" name="type_file" id="formatTXT" value="txt" required />TXT </Label>
            </div>
              <Button type="submit" >Extraer Receta</Button>
          </Form>
        </ContainerForm>

      </Container>
    </>

  );
}

export default Main;