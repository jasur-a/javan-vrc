import React  from 'react';

import { Modal } from '../../ui/modal';

/**
 * @render react
 * @name ModalWrapper
 * @description ModalWrapper Component for Javan
 * @example
 * <Modal> This is a modal</Modal>
 */

export const ModalWrapper = (props) => {
  const  { modal, show, handleShowModal } = props

  return (
    <Modal
      onOpen={show}
      onClose={handleShowModal}
      {...modal}
    />
  );
};

export default ModalWrapper;
