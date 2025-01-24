const API_URL = 'http://localhost:8000/api/auth/token';

interface TokenData {
  username: string;
  password: string;
}

const getToken = async (data: TokenData, setErrorMessage: React.Dispatch<React.SetStateAction<string>>) => {
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
      if (response.status === 400 || response.status === 401) {
        setErrorMessage('Email and/or password are incorrect.')
      }
      throw new Error('Token generation failed');
    }

    return responseData;
  } catch (error) {
    console.error('Error fetching token:', error);
    throw new Error('Token generation failed');
  }
};

export default getToken;