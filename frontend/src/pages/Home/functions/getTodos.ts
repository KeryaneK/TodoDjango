const API_URL = 'http://localhost:8000/api/todos';

const getTodos = async (token: string) => {
    try {
        const response = await fetch(API_URL, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token
          },
        });
    
        const responseData = await response.json();
    
        return responseData;
      } catch (error) {
        console.error('Error fetching token:', error);
        throw new Error('Token generation failed');
      }
}

export default getTodos