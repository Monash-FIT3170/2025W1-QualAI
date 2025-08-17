import React, { useState } from 'react';
import DropZone from './DropZone';

const TestPage: React.FC = () => {
  const [files, setFiles] = useState<File[]>([]);
  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 24 }}>
      <h2>DropZone Test</h2>
      <DropZone onFilesDropped={setFiles} />
      <ul>
        {files.map((file, idx) => (
          <li key={idx}>
            {file.name}
            {file.type.startsWith("audio/") && (
              <audio controls src={URL.createObjectURL(file)} style={{ marginLeft: 10 }} />
            )}
            {file.type.startsWith("image/") && (
              <img src={URL.createObjectURL(file)} alt={file.name} style={{ maxHeight: 40, marginLeft: 10 }} />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TestPage;