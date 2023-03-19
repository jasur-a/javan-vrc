import { useEffect, useState } from 'react';

/**
 * @name UploadFileController
 * @description Controller UploadVideo
 * @params { props }
 * @return { Object }
 */

export const UploadVideoController = (props) => {
  console.log("::props", props)
  const {
    name = '',
    supported_filetype = ['mp4', 'mov'],
    compress_quality = 0.9,
    form,
    formState
  } = props;

  const valueForm = form[name];

  const vid_ext = ['mp4', 'mov'];

  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');
  const [fileName, setFileName] = useState('');
  const [fileType, setFiletype] = useState('');
  const [loading, setLoading] = useState(false);

  const quality = compress_quality;
  const compress_from = 2097152;

  useEffect(() => {
    const val_back =
      typeof valueForm === 'object' && valueForm[name]
        ? valueForm[name]
        : valueForm;

    if (val_back && typeof val_back === 'string') {
      var value_split = val_back.split('/')[2];
      setFileName(value_split);
      setFiletype(value_split.split('.')[1]);
    }
  }, [valueForm, name]);

  // handle drag events
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!loading) {
      if (e.type === 'dragenter' || e.type === 'dragover') {
        setDragActive(true);
      } else if (e.type === 'dragleave') {
        setDragActive(false);
      }
    }
  };

  // triggers when file is dropped
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (!loading) {
      setDragActive(false);
      let { files = [] } = e.dataTransfer;
      if (files && files[0]) {
        handleFiles(files[0]);
      }
    }
  };

  // triggers when file is selected with click
  const handleChange = (e) => {
    e.preventDefault();
    let { files = [] } = e?.target;
    if (files && files[0]) {
      handleFiles(files[0]);
    }
  };

  const handleFiles = async (file) => {
    setLoading(true);

    const { size, type } = file;
    const ext = type.split('/')[1];
    var error_msg = '';
    var new_file = file;

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
        let file_base64 = await getBase64(new_file);

        if (file_base64) {
          formState({...FormData, [name]: file_base64})
        }
      } catch (err) {
        setError('Hubo un error con el video, por favor súbalo de nuevo');
        console.error(err);
      }
      setLoading(false);
    }
  };

  const getBase64 = (file) => {
    return new Promise((resolve) => {
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        resolve(reader.result);
      };
    });
  };

  return {
    handleDrag,
    handleDrop,
    handleChange,
    name,
    fileName,
    fileType,
    error,
    dragActive,
    loading
  };
};
