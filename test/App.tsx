import React, { useState } from 'react';
import TranscriptEditor from '../src/TranscriptEditor';

const App: React.FC = () => {
  const [transcript, setTranscript] = useState<{
    html: string;
    text: string;
  }>({
    html: `<p>Interviewer: Thank you for joining us today. Could you start by introducing yourself and your role?</p>
<p>Participant: Sure, I'm Dr. Jane Smith, a cognitive psychologist specializing in decision-making processes. I've been researching this field for about 15 years now.</p>
<p>Interviewer: That's fascinating. Could you tell us more about your current research focus?</p>
<p>Participant: My team is currently exploring how environmental factors influence split-second decisions. We're particularly interested in how lighting, ambient noise, and spatial arrangement can impact critical choices in emergency situations.</p>`,
    text: 'Interviewer: Thank you for joining us today. Could you start by introducing yourself and your role?\n\nParticipant: Sure, I\'m Dr. Jane Smith, a cognitive psychologist specializing in decision-making processes. I\'ve been researching this field for about 15 years now.\n\nInterviewer: That\'s fascinating. Could you tell us more about your current research focus?\n\nParticipant: My team is currently exploring how environmental factors influence split-second decisions. We\'re particularly interested in how lighting, ambient noise, and spatial arrangement can impact critical choices in emergency situations.',
  });

  const handleSave = (content: { html: string; text: string }) => {
    // In a real app, this would be an API call
    console.log('Saving transcript:', content);
    setTranscript(content);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white shadow-sm py-3 px-6 border-b border-gray-200">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-semibold text-gray-800">Qualitative Research Analysis</h1>
          <div className="text-sm">
            <span className="text-blue-600">Transcript #123456</span>
          </div>
        </div>
      </header>

      <main className="flex-grow p-6 overflow-hidden">
        <div className="max-w-7xl mx-auto h-full flex flex-col">
          <TranscriptEditor initialContent={transcript.html} onSave={handleSave} />
        </div>
      </main>

      <footer className="bg-white py-2 px-6 border-t border-gray-200 text-sm text-gray-500">
        <div className="max-w-7xl mx-auto">
          <span>AI-Powered Qualitative Research Tool</span>
        </div>
      </footer>
    </div>
  );
};

export default App;