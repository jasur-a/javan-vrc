import styled from 'styled-components';


export const Container = styled.div`
  text-align: center;
  width: 100%;
  display: flex;
  position: relative;
  z-index: 3;
  height: 100%;
  justify-content: center;
  background-color: #02566c;
  align-items: center;
  padding: 0px;
  flex-direction: column;
  min-height: 100vh;
`;

export const ContainerForm = styled.div`
  width: 90vw;
  display: flex;
  height: auto;
  margin: 20px auto 50px;
  max-width: 619px;
  border-radius: 15px;
  background: #fff;
  position: relative;
  min-height: 72px;
  flex-direction: column;
  max-height: 90%;
  padding: 20px;
`;


export const Header = styled.div`
  padding: 20px 9% 40px ;
  color: #fff;
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

export const Button  = styled.button`
  background: #02566c;
  color: #fff;
  border: 1px solid #02566c;
  padding: 20px;
  margin: auto;
  position: relative;
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  cursor:pointer;
`

export const Input = styled.input`
  border: 1px solid #333;
  background: #fff;
  height: 40px;
  display: block;
  width: 100%;
  border-radius: 10px;

  &[type='checkbox'], &[type='radio']{
    height: 20px;
    display: inline-block;
    width: auto;
    margin-right: 15px;

  }
`;

export const Label = styled.label`
  display: flex;
  align-items: center;

  & .link{
    background: none;
    border: none;
    text-decoration: underline;
    color: #02566c;
    font-weight: 600;
    font-size: initial;
    cursor: pointer;
  }
`;