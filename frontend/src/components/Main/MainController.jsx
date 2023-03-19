import React, {  useState } from 'react';
import { handleUploadImage } from '../../api/api';

export function MainController (props) {

  const [ showModal, setShoModal] = useState(false);
  const [ formData, setFormData] = useState({});
  const [ disabled, setDisabled] = useState({"url": false, "fileUpload": false});

  const handleSubmit = async (ev)  => {
    ev.preventDefault();

    const response = await handleUploadImage(formData)

    if(response){
      console.log("::response", response)
    }
  }


  const handleChangeForm = (e) => {
    const { target : { value, name, files } = {}} = e;
    let val;

    switch(name){
      case "url":
        if( value !== ""){
        val = value;
          setDisabled({...disabled, "fileUpload": true})
        }else{
          setDisabled({...disabled, "fileUpload": false})
        }
        break;
      case "fileUpload":
        if( value !== ""){
          val = files[0]
          setDisabled({...disabled, "url": true})
        }else{
          setDisabled({...disabled, "url": false})
        }
        break;
      default:
        val = value;
        break;
    }

    if(val){
      setFormData({...formData, [name] : val})
    } else {
      delete formData[name]
    }
  }

  return {
    handleChangeForm,
    handleSubmit,
    showModal, setShoModal,
    formData, setFormData,
    disabled, setDisabled
  };
}
