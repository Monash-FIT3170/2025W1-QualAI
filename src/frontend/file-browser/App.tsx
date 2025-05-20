import React from 'react';
import UploadFileButton from '../chatbot/src/components/UploadFileButton';
import BrowseFolderButton from './BrowseFolderButton';

const App: React.FC = () => {
  const handleFileSelected = (file: File) => {
    console.log("Selected file:", file.name);
    // You can send the file to a backend here
  };

  return (
    <div className='App'>
      <UploadFileButton onFileSelected={handleFileSelected} />
    </div>
  );
};

export default App;