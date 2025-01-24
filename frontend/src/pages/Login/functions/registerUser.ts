import getToken from "./getToken";

const API_URL = 'http://localhost:8000/api/auth/register';

interface RegisterData {
  email: string;
  password: string;
}

const registerUser = async (data: RegisterData, setErrorMessage: React.Dispatch<React.SetStateAction<string>>) => {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const responseData = await response.json();

    if (!response.ok) {
      if (responseData.email) {
        setErrorMessage(responseData.email[0]);
      }
      if (responseData.password) {
        setErrorMessage(responseData.password[0])
      }
      throw new Error('Registration failed');
    }

    const token = await getToken({'username': data.email, "password": data.password}, setErrorMessage);
    return token;
  } catch (error) {
    throw new Error('Registration failed');
  }
};

export default registerUser;