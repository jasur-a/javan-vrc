import { useState } from 'react';

/**
 * @name UploadFileController
 * @description Controller UploadVideo
 * @params { props }
 * @return { Object }
 */

export const UploadVideoController = (props) => {
  const {
    name = '',
    supported_filetype = ['mp4'],
    formState
  } = props;


  const [error, setError] = useState('');
  const [fileName, setFileName] = useState('');
  const [loading, setLoading] = useState(false);


  // triggers when file is selected with click
  const handleChange = (e) => {
    e.preventDefault();
    let { files = [] , value = ""} = e?.target;
    if (files && files[0]) {
      handleFiles(files[0], value);
    }
  };

  const handleFiles = async (file, value) => {
    setLoading(true);

    const { type } = file;
    const ext = type.split('/')[1];
    var error_msg = '';

    setError(error_msg);

    if (!supported_filetype.includes(ext)) {
      error_msg = `${error_msg} Formato no permitido, solo se acepta: ${supported_filetype.join(
        ', '
      )}. `;
    }

    if (error_msg !== '') {
      setError(error_msg);
      setLoading(false);
    } else {

      setError('');

      try {
        
          setFileName(file?.name);
          formState({...FormData, [name]: file})
      } catch (err) {
        setError('Hubo un error con el video. Por favor súbalo de nuevo');
        console.error(err);
      }
      setLoading(false);
    }
  };

  return {
    handleChange,
    name,
    fileName,
    error,
    loading
  };
};
