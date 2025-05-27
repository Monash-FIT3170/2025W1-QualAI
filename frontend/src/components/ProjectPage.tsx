
import Sidebar from './Sidebar';
import Chatbot from './Chatbot';
import RichTextEditor from '@/editor/RichTextEditor';
import { useState, useEffect } from 'react';


const ProjectPage = () => {
  const [files, setFiles] = useState<{ key: string }[]>([]);
  const [selectedFileContent, setSelectedFileContent] = useState('');
  const [selectedFileKey, setSelectedFileKey] = useState<string | null>(null);

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
        setSelectedFileKey(fileKey); // Set the selected file key
      })
      .catch(console.error);
  };

  const handleFileDelete = (fileKey : string) : void => {
      if ( selectedFileKey == fileKey ) {
          setSelectedFileContent("");
          setSelectedFileKey(null);
      }
  }

  return (
    <div className="min-h-screen flex">
      <Sidebar 
      files={files}
      onFileSelect={handleFileSelect}
      onFileDelete={handleFileDelete}
      onRefreshFiles={fetchFiles}/>
      <main className="flex-1 p-6">
        <RichTextEditor initialContent={selectedFileContent} fileKey={selectedFileKey} />
      </main>
      <Chatbot />
    </div>
  );
};

export default ProjectPage;
