import  { useEffect, useState } from 'react';
import { generate_recipe , get_recipes } from '../../api/api';

export function MainController (props) {

  console.log("::props", props)
  const [ showModal, setShoModal] = useState(false);
  const [ formData, setFormData] = useState({});
  const [ disabled, setDisabled] = useState({"url": false, "fileUpload": false});

  useEffect( () => {

    console.log("::list", get_recipes())


  }, [])

  const handleSubmit = async (ev)  => {
    ev.preventDefault();

    const response = await generate_recipe(formData)

    if(response){
      console.log("::response", response)

      return response
    }
  }





  const handleChangeForm = (e) => {
    const { target : { value, name, files , checked } = {}} = e;
    let val;

    console.log("::e", e)

    console.log("::val", val)
    console.log("::val", checked)

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
          val = value
          setDisabled({...disabled, "url": true})
        }else{
          setDisabled({...disabled, "url": false})
        }
        break;
      default:
        val = value;
        break;
    }
    if(checked){
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
    disabled, setDisabled
  };
}
