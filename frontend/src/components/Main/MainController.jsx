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


  const handleChangeForm = (e) => {
    const { target : { value, name, files, checked, type } = {}} = e;
    let val;

    console.log("::e", e)
    console.log("::file", files)
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
