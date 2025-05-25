import axios from 'axios';
/**
 * @file chat_client.ts
 * @author Rohan Shetty
 * @description API client for communicating with the backend chatbot service
 */

// Base configuration for axios instance
const API_URL = 'http://127.0.0.1:5001'

/**
 * Axios instance configured for chatbot API requests
 * 
 * @constant
 * @type {AxiosInstance}
 * 
 * @property {string} baseURL - The base URL for all API requests
 * @property {number} timeout - Request timeout in milliseconds
 */
const instance = axios.create({
    baseURL: API_URL,
    timeout: 1000000, // 1000 seconds timeout
  });

  /**
   * Sends a user message to the chatbot API and returns the AI response
   * 
   * @async
   * @function fetchChat
   * @param {string} message - The user's message to send to the chatbot
   * @returns {Promise<string>} The AI's response text
   * @throws {Error} When the API request fails or returns an error
   * 
   */
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