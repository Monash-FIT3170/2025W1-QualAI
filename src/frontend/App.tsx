import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Chatbot from './components/Chatbot';
import UploadFileButton from './components/UploadFileButton';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto p-4">
        <UploadFileButton/>
        <Chatbot/>
      </div>
    </div>
  );
}

export default App;