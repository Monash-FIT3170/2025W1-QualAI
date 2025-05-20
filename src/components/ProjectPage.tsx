
import Sidebar from './Sidebar';
import Chatbot from './Chatbot';
import RichTextEditor from '@/editor/RichTextEditor';

const ProjectPage = () => {
  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <main className="flex-1 p-6">
        <RichTextEditor />
      </main>
      <Chatbot />
    </div>
  );
};

export default ProjectPage;
