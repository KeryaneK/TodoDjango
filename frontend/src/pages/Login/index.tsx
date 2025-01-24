import {useState, useRef} from 'react'
import registerUser from './functions/registerUser';
import getToken from './functions/getToken';
import Cookies from 'js-cookie'
import { useNavigate } from 'react-router-dom'
import './index.css'

const Login = () => {
  const navigate = useNavigate();

  const login = useRef<HTMLInputElement | null>(null);
  const password = useRef<HTMLInputElement | null>(null);
  const repeatedPassword = useRef<HTMLInputElement | null>(null);

  const [isRegistering, setIsRegistering] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');


  return (
  <div className='login'>
    <div className='loginWindow'>
      <label>Email</label>
      <input ref={login} type='text'></input>
      <label>Password</label>
      <input ref={password} type='password'></input>
      {isRegistering && <>
        <label>Repeat password</label>
        <input ref={repeatedPassword} type='password'></input>
      </>}
      <div className='loginButtons'>
        {isRegistering ? 
        <>
          <button onClick={async () => {
            if (password.current!.value !== repeatedPassword.current!.value) {
              setErrorMessage('Passwords do not match!');
              return;
            }
            const token = await registerUser({'email': login.current!.value, 'password': password.current!.value}, setErrorMessage)
            if (token.token) {
              Cookies.set('auth', token.token, { expires: 1 });
              navigate('/');
            }
          }} id='loginButton'>
            Register
          </button>
          <button onClick={() => {setIsRegistering(!isRegistering); setErrorMessage('')}} id='registerButton'>
            Login
          </button>
        </> :
        <>
          <button onClick={async () => {
            const token = await getToken({'username': login.current!.value, 'password': password.current!.value}, setErrorMessage);
            if (token.token) {
              Cookies.set('auth', token.token, { expires: 1 });
              navigate('/');
            }
          }} id='loginButton'>
            Login
          </button>
          <button onClick={() => {setIsRegistering(!isRegistering); setErrorMessage('')}} id='registerButton'>
            Register
          </button>
        </>}
      </div>
      <div className='overlay'>
        {errorMessage}
      </div>
    </div>
  </div>
  )
}

export default Login