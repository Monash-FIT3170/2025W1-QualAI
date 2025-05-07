import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000'

const instance = axios.create({
    baseURL: API_URL,
    timeout: 1000000,
  });

  export const fetchChat = async (message: string): Promise<string> => {
    try {
      const response = await instance.post('/chat',
        {
          message: message,
        },
      );
      return response.data.response;
    } catch (error: any) {
      console.error('Error getting chat response: ', error);
      throw error;
    }
  };