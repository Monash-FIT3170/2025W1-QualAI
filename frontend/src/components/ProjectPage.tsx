import Sidebar from './Sidebar';
import Chatbot from './Chatbot';
import RichTextEditor from '@/editor/RichTextEditor';
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft } from 'lucide-react';


const ProjectPage = () => {
    const { projectName } = useParams<{ projectName : string }>();
    const navigate = useNavigate();
    const [ files, setFiles ] = useState<{ key : string }[]>([]);
    const [ selectedFileContent, setSelectedFileContent ] = useState('');
    const [ selectedFileKey, setSelectedFileKey ] = useState<string | null>(null);

    const fetchFiles = () => {
        fetch(`http://localhost:5001/${projectName}/documents`)
            .then(res => res.json())
            .then(data => setFiles(data))
            .catch(console.error);
    };

    useEffect(() => {
        fetchFiles();
    }, []);

    // This function will be passed to Sidebar, triggered when a file is clicked
    const handleFileSelect = (fileKey : string) => {
        fetch(`http://localhost:5001/${projectName}/documents/${ fileKey }`) // Adjust URL and endpoint as needed
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
        <div className="min-h-screen bg-black flex flex-col">
            {/* Header */}
            <header className="bg-black border-b border-gray-700 px-6 py-4">
                <div className="flex items-center space-x-4">
                    <button 
                        onClick={() => navigate('/')}
                        className="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors"
                    >
                        <ArrowLeft size={20} />
                        <div className="flex items-center space-x-2">
                            <img src="/Logo.png" alt="QualAI" className="w-8 h-8 object-contain" />
                            <span className="text-sm font-medium">QualAI</span>
                        </div>
                    </button>
                    <div className="h-6 w-px bg-gray-600"></div>
                    <h1 className="text-xl font-semibold text-white">
                        {projectName ? decodeURIComponent(projectName) : 'Current Project Name'}
                    </h1>
                </div>
            </header>

            {/* Main Content */}
            <div className="flex-1 flex">
                <Sidebar
                    files={ files }
                    onFileSelect={ handleFileSelect }
                    onFileDelete={ handleFileDelete }
                    onRefreshFiles={ fetchFiles }
                />
                <main className="flex-1 bg-black">
                    <RichTextEditor 
                        initialContent={ selectedFileContent } 
                        fileKey={ selectedFileKey ?? undefined }
                        projectName={ projectName ?? undefined }
                    />
                </main>
                <Chatbot/>
            </div>
        </div>
    );
};

export default ProjectPage;
