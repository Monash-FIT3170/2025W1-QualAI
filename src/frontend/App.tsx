import './App.css'
import Chatbot from "./chatbot/components/Chatbot";
import UploadFileButton from "./chatbot/components/UploadFileButton";


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