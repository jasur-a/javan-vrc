import React from 'react';
import {
  UploadFileContainer,
  InputError,
  Label,
  Button,
  Spinner
} from './UploadVideo.style';
import { UploadVideoController } from './UploadVideoController';

/**
 * @render react
 * @name UploadFile
 * @description UploadVideo Component
 * @example
 *  <UploadVideo> This is a switch</UploadVideo>
 */

export const UploadVideo = (props) => {
  const {
    label = '',
    placeholder = '',
    style,
    disabled = false,
    ...rest
  } = props;

  const {
    handleChange,
    name,
    fileName,
    error,
    loading
  } = UploadVideoController(props);

  return (
    <UploadFileContainer
      key={name}
      data={name}
      className={loading ? 'disabled' : ''}
    >
      <div id='file-upload' >
        <input
          type='file'
          id={name}
          onChange={handleChange}
          name={name}
          disabled={disabled || loading}
        />
        <Label htmlFor={name}>
          <div>
            <p>{label && label}</p>
            {fileName !== '' && <p>{fileName}</p>}
            {placeholder && fileName === '' && <p>{placeholder}</p>}
          </div>
          <Button >
            {loading ? <Spinner /> : <>Subir</>}
          </Button>
        </Label>
      </div>
      {error !== '' && (
        <InputError >
          {rest?.iconMsgError && (
            <img alt='Error icon' src={rest?.iconMsgError} />
          )}
          {error}
        </InputError>
      )}
    </UploadFileContainer>
  );
};

export default UploadVideo;
