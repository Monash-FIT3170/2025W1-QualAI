
import Sidebar from './Sidebar';
import Editor from './Editor';
import Chatbot from './Chatbot';

const ProjectPage = () => {
  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <main className="flex-1 p-6">
        <Editor />
      </main>
      <Chatbot />
    </div>
  );
};

export default ProjectPage;
