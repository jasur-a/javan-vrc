import React from 'react';
import { modalLegals } from '../constants/constants';
import ModalWrapper from '../core/modalWrapper/ModalWrapper';
import { UploadVideo } from '../core/uploadVideo';
import { MainController } from './MainController';
import {  Container, Form, Input, Label } from './Main.style';

export function Main (props) {

  const {
    handleChangeForm,
    handleSubmit,
    showModal, setShoModal,
    formData, setFormData,
    disabled
  } = MainController(props)

  return (

      <Container>
        <ModalWrapper modal={modalLegals} show={showModal}  handleShowModal={setShoModal} />
        <h3>Por favor indique el origen de su video</h3>
        <Form onSubmit={handleSubmit} onChange={handleChangeForm }>
          <div>
            <Label htmlFor="url">Por url (indique la url de youtube)</Label>
            <Input type="text"  name="url" disabled={disabled.url}/>

          </div>
          <div>
            <Label htmlFor="fileUpload">Subir desde el ordenador </Label>
            <UploadVideo name="fileUpload" disabled={disabled.fileUpload} form={formData} formState={setFormData}/>

          </div>

          <div>
            <Label htmlFor="legals"> <Input type="checkbox" className="checkbox" name="legals"  id="legals" disabled={disabled.fileUpload} /> Acepto las <button type="button" onClick={() => setShoModal(true)}>políticas de uso </button> </Label>
          </div>

          <div>
            <Label htmlFor="is_mexican"> <Input type="checkbox" className="checkbox" name="is_mexican" id="is_mexican" />La receta ingresada es de comida Mexicana  </Label>
          </div>

          <div>
            <button>Extraer Receta</button>
          </div>
        </Form>
      </Container>
  );
}

export default Main;