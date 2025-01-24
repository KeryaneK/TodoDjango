import {useState, useEffect} from 'react'
import { useNavigate } from 'react-router-dom'
import Cookies from 'js-cookie'

const Home = () => {
  const navigate = useNavigate();
  const [token, setToken] = useState('');

  //const [todos, setTodos] = useState([]);

  useEffect(() => {
    const token = Cookies.get('auth');
    if (token) {
      setToken(token);
    } else {
      navigate('/login')
    }
  }, []);

  return (
    <div>{token}</div>
  )
}

export default Home