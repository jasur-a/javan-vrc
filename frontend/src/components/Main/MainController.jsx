import  { useEffect, useState } from 'react';
import { generate_recipe , get_recipes, download_recipe } from '../../api/api';

export function MainController (props) {

  const [ showModal, setShoModal] = useState(false);
  const [ formData, setFormData] = useState({});
  const [ listRecipes, setListRecipes] = useState([]);
  const [ disabled, setDisabled] = useState({"url": false, "fileUpload": false});

  useEffect( () => {
    getRecipes()
  }, [])


  const getRecipes = async ()  => {
    const response = await get_recipes();
    if(response){
      setListRecipes(response)
      return response
    }
  }

  //TODO descargar el file data = {id, type_file}
  const handleDownloadFile = async (ev, data)  => {
    ev.preventDefault();

    const response = await download_recipe(data)

    if(response){
      console.log("::response", response)

      return response
    }
  }


  const handleSubmit = async (ev)  => {
    ev.preventDefault();

    const response = await generate_recipe(formData)

    if(response){
      console.log("::response", response)

      return response
    }
  }


  const getBase64 = (file) => {
    return new Promise((resolve) => {
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        resolve(reader.result);
      };
    });
  };

  const handleChangeForm = async (e) => {
    const { target : { value, name, files, checked, type } = {}} = e;
    let val;

    switch(name){
      case "url":
        if( value !== ""){
        val = value;
          setDisabled({...disabled, "file_upload": true})
        }else{
          setDisabled({...disabled, "file_upload": false})
        }
        break;
      case "file_upload":
        if( value !== ""){
          let file_base64 = await getBase64(files[0]);
          val = file_base64
          setDisabled({...disabled, "url": true})
        }else{
          setDisabled({...disabled, "url": false})
        }
        break;
      default:
        val = value;
        break;
    }

    if(checked && type === 'checkbox'){
      val = checked
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
    disabled, setDisabled,
    listRecipes
  };
}
