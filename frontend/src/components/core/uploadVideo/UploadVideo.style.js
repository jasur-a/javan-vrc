import styled, { keyframes } from 'styled-components';

export const UploadFileContainer = styled.div`
  #file-upload {
    position: relative;
    margin-bottom: 15px;
    padding: 0rem 0.5rem;
    background: #fff;
    cursor: pointer;
    border: 1px solid #333;
    height: 50px;
    display: block;
    border-radius: 10px;

  input {
    display: none;
  }

  &.disabled {
    * { cursor: no-drop; }
    label {
      cursor: no-drop;
    }
  }

`;

export const Button = styled.span`
  cursor: pointer;
  padding-left: 10px;
  font-size: 1rem;
  border: none;
  font-family: inherit;
  background-color: transparent;
  color:#333;
  text-decoration-line: underline;

`;

export const Label = styled.label`
  height: 100%;
  display: flex;
  align-items: center;
  width: 100%;
  display: flex;
  justify-content: space-between;
  cursor: pointer;
  text-align: left;
  vertical-align: middle;
  position: relative;

  & p {
    margin-top: 0;
    margin-bottom: 0;
    font-size: 13px;
  }

  & div > p:first-child {
    color: #333;
    font-weight: 500;
  }

  & img {
    padding-right: 10px;
  }


`;

export const InputError = styled.p`
  color: #333;
  display: inline;
  line-height: 1;
  margin-bottom: 15px;
  font-size: 0.75rem;
  width: 100%;
`;

const spin = keyframes`
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
`;

export const Spinner = styled.div`
  border: 3px solid rgba(0, 0, 0, 0.1);
  width: 20px !important;
  height: 20px !important;
  margin-right: 5px;
  border-radius: 50%;
  border-left-color: #333;
  animation: ${spin} 1s ease infinite;
`;
