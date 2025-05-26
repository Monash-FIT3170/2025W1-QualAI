
import Sidebar from './Sidebar';
import Chatbot from './Chatbot';
import RichTextEditor from '@/editor/RichTextEditor';
import React, { useState, useEffect } from 'react';


const ProjectPage = () => {
  const [files, setFiles] = useState<{ key: string }[]>([]);
  const [selectedFileContent, setSelectedFileContent] = useState('');

  const fetchFiles = () => {
    fetch('http://localhost:5001/documents')
      .then(res => res.json())
      .then(data => setFiles(data))
      .catch(console.error);
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  // This function will be passed to Sidebar, triggered when a file is clicked
  const handleFileSelect = (fileKey: string) => {
    fetch(`http://localhost:5001/documents/${fileKey}`) // Adjust URL and endpoint as needed
      .then(res => res.json())
      .then(data => {
        setSelectedFileContent(data.content); // Set content for editor
      })
      .catch(console.error);
  };

  return (
    <div className="min-h-screen flex">
      <Sidebar 
      files={files}
      onFileSelect={handleFileSelect}
      onRefreshFiles={fetchFiles}/>
      <main className="flex-1 p-6">
        <RichTextEditor initialContent={selectedFileContent} />
      </main>
      <Chatbot />
    </div>
  );
};

export default ProjectPage;
