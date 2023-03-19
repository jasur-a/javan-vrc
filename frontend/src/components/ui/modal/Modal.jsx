import React from 'react';
import {
  ModalContainer,
  Modals,
  Close,
  ModalBody,
  ModalFooter,
  HeadTitle,
} from './Modal.styled';

/**
 * @render react
 * @name Modal
 * @description Modal Component
 * @example
 */

/*
  ej del objeto ==>
  {
    "header": {
      "title":"<h5>titulo<h5>",
    },
    "body": {
      "children":"<p> esto es  el body</p>",
    },
    "footer": {
      "children":"<p> esto es el footer</p>",
    }
  }
*/

const IconClose = (
  <svg
    xmlns='http://www.w3.org/2000/svg'
    height='26'
    width='26'
    viewBox='0 0 24 24'
  >
    <path d='M0 0h24v24H0z' fill='none' />
    {/* eslint-disable max-len */}
    <path d='M14.606 12l3.91-3.909c.479-.48.479-1.257 0-1.737l-.87-.87c-.48-.479-1.257-.479-1.737 0L12 9.395l-3.909-3.91c-.48-.479-1.257-.479-1.737 0l-.87.87c-.479.48-.479 1.257 0 1.737L9.395 12l-3.91 3.909c-.479.48-.479 1.257 0 1.737l.87.87c.48.479 1.257.479 1.737 0L12 14.605l3.909 3.91c.48.479 1.258.479 1.737 0l.87-.87c.479-.48.479-1.257 0-1.737L14.605 12z' />
    {/* eslint-enable max-len */}
  </svg>
);
export function Modal(props) {
  const {
    onOpen,
    onClose,
    header,
    body,
    footer,
    ...rest
  } = props;
  const createMarkup = (data) => ({ __html: data });

  return (
    <>
      {onOpen && (
        <ModalContainer
          {...rest}
          data-cy='modal'
        >
          <Modals>
            <Close
              onClick={() => onClose(false)}
              className='ModalClose'
            >
              { IconClose }
            </Close>
            {header && (
              <HeadTitle
                dangerouslySetInnerHTML={createMarkup(header?.title)}
              ></HeadTitle>
            )}
            {body &&  (
              <ModalBody
                dangerouslySetInnerHTML={createMarkup(body?.children)}
              ></ModalBody>
            )}
            {footer && (
              <ModalFooter
                dangerouslySetInnerHTML={createMarkup(footer?.children)}
              ></ModalFooter>
            )}
          </Modals>
        </ModalContainer>
      )}
    </>
  );
}

export default Modal;
