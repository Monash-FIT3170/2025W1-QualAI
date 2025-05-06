import React from 'react';
import UploadFileButton from './UploadFileButton';
import BrowseFolderButton from './BrowseFolderButton';

const App: React.FC = () => {
  const handleFileSelected = (file: File) => {
    console.log("Selected file:", file.name);
    // You can send the file to a backend here
  };
  const handleFilesSelected = (files: FileList) => {
    console.log("Selected folder files:");
    for (const file of files) {
      console.log("Selected file:", file.name);
      // You can send each file to a backend here
    }
  };

  return (
    <div className='App'>
      <UploadFileButton onFileSelected={handleFileSelected} />
      <BrowseFolderButton onFilesSelected={handleFilesSelected} />
    </div>
  );
};

export default App;