import styled from 'styled-components';

export const ModalContainer = styled.div`
  width: 100%;
  display: flex;
  position: fixed;
  z-index: 3;
  height: 100%;
  justify-content: center;
  background-color: rgba(0,0,0,.5);
  align-items: center;
  left: 0px;
  right: 0px;
  top: 0px;
  bottom: 0px;
`;

export const Modals = styled.div`
  width: 90%;
  display: flex;
  height: auto;
  margin: 0px;
  max-width: 619px;
  border-radius: 24px;
  background: #ffffff;
  position: relative;
  min-height: 72px;
  flex-direction: column;
  max-height: 90%;

  & > div:not(.ModalClose) {
    padding-left: 30px;
    padding-right: 30px;
  }
  & div:nth-child(2) {
    padding-top: 42px;
  }
  & div:last-child {
    padding-bottom: 34px;
    border-radius: 0 0 24px 24px;
  }
  @media (max-height: 500px) {
    overflow-y: auto;
  }
`;

export const Close = styled.div`
  fill: #333;
  padding: 11.5px 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  line-height: 0px;
  position: absolute;
  margin-right: 4px;
  text-align: right;
  right: 0px;
  top: 4px;
  cursor: pointer;
  z-index: 1;
`;

export const HeadTitle = styled.div`
  font-size: 22px;
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: normal;
  text-align: left;
  color: #554a48;
  padding: 10px 30px;
`;

export const ModalBody = styled.div`
  padding: 10px 30px 0px;
  text-align: left;
  font-size: 16px;
  line-height: 1.5;
  color: #393130;
  & p {
    line-height: 1.5;
  }
  & strong {
    font-weight: bold;
  }

`;

export const ModalFooter = styled.div`
  padding: 10px 30px;
  text-align: left;
  font-size: 16px;
  line-height: 1.4;
  color: #393130;
`;

export const ModalsClose = styled.div`
  width: 100%;
  position: absolute;
  height: 100vh;
  z-index: 0;
`;
