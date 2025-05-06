import { useNavigate } from 'react-router-dom';
import { Plus, Folder } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 space-y-8">
      <div className="text-center space-y-4">
        <h2 className="text-2xl font-light text-gray-400">Analyze Interviews with AI</h2>
        
        <div className="w-24 h-24 mx-auto">
          <img src="/Logo.png" alt="QualAI Logo" className="w-full h-full object-cover" />
        </div>

        <h1 className="text-5xl font-bold mb-2">QualAI</h1>
        <p className="text-gray-400 text-xl">
          Transcribe and thematically analyze qualitative interview data
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 mt-8">
        <div className="text-center">
          <button 
            onClick={() => navigate('/project/new')} 
            className="btn-primary mb-2"
          >
            <Plus size={20} />
            New Project
          </button>
          <p className="text-sm text-gray-400">Start from scratch</p>
        </div>

        <div className="text-center">
          <button 
            onClick={() => navigate('/project')} 
            className="btn-secondary mb-2"
          >
            <Folder size={20} />
            Open Project
          </button>
          <p className="text-sm text-gray-400">Load existing work</p>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
