import styled from 'styled-components';


export const Container = styled.div`
  width: 100vw;
  display: flex;
  height: auto;
  margin: auto;
  max-width: 619px;
  border-radius: 15px;
  background: #fff;
  position: relative;
  min-height: 72px;
  flex-direction: column;
  max-height: 90%;
  padding: 20px;
`;


export const Form = styled.form`
  width: 100%;
  display: flex;
  max-width: 619px;
  flex-direction: column;
  justify-content: start;
  text-align: left;

  & > div {
    margin-bottom: 15px;
  }
`;

export const Input = styled.input`
  border: 1px solid #333;
  background: #fff;
  height: 40px;
  display: block;
  width: 100%;
  border-radius: 10px;

  &[type='checkbox']{
    height: 20px;
    display: inline-block;
    width: auto;
    margin-right: 15px;

  }
`;

export const Label = styled.label`
  display: flex;
  align-items: center;
`;