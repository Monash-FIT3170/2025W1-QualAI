import { useNavigate } from "react-router-dom";
import { Plus, FolderOpen } from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";

const LandingPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [projectName, setProjectName] = useState("");
  const [projects, setProjects] = useState<string[]>([]);

  useEffect(() => {
    fetch("http://localhost:5001/projects")
        .then((res) => res.json())
        .then((data) => setProjects(data.projects))
        .catch(console.error);
  }, []);

  const handleCreateProject = async () => {
    if (!projectName.trim()) {
      toast.error("Please enter a project name");
      return;
    }

    setLoading(true);

    try {
      const encoded = encodeURIComponent(projectName);
      const res = await fetch(`http://localhost:5001/project/${encoded}`, {
        method: "POST",
      });

      if (!res.ok) throw new Error("Failed to create project");

      toast.success(`Project "${projectName}" created!`);
      navigate(`/project/${encoded}`);
    } catch (err) {
      console.error(err);
      toast.error("Could not create project");
    } finally {
      setLoading(false);
    }
  };

  return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center p-6 space-y-10">
        <div className="text-center space-y-6">
          <h2 className="text-2xl font-light text-white italic">
            Analyze Interviews with AI
          </h2>

          <div className="w-32 h-32 mx-auto p-2 bg-black rounded-lg">
            <img
                src="/Logo.png"
                alt="QualAI Logo"
                className="w-full h-full object-contain"
            />
          </div>

          <h1 className="text-5xl font-bold mb-2 text-white">QualAI</h1>
          <p className="text-white text-xl">
            Transcribe and thematically analyze qualitative interview data
          </p>
        </div>

        <div className="flex flex-row gap-8 w-full max-w-3xl">
          <div className="flex-1 bg-gray-900/50 backdrop-blur border border-gray-700/50 shadow-2xl rounded-2xl p-8 text-center hover:bg-gray-900/70 transition-all duration-300">
            <div className="mb-6">
              <div className="w-14 h-14 mx-auto mb-4 bg-gradient-to-r from-green-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
                <Plus size={28} className="text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">New Project</h3>
              <p className="text-gray-400 text-sm">Start from scratch</p>
            </div>

            <input
                type="text"
                placeholder="Enter project name..."
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="px-4 py-3 bg-gray-800/50 border border-gray-600 text-white placeholder-gray-400 rounded-xl w-full mb-6 text-center focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                disabled={loading}
                onKeyDown={(e) => e.key === 'Enter' && handleCreateProject()}
            />

            <button
                onClick={handleCreateProject}
                className={`w-full py-3 px-6 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-medium rounded-xl transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transform hover:scale-105 ${
                    loading ? "opacity-50 cursor-not-allowed transform-none" : ""
                }`}
                disabled={loading}
            >
              {loading ? "Creating..." : "Create Project"}
            </button>
          </div>

          <div className="flex-1 bg-gray-900/50 backdrop-blur border border-gray-700/50 shadow-2xl rounded-2xl p-8 text-center hover:bg-gray-900/70 transition-all duration-300">
            <div className="mb-6">
              <div className="w-14 h-14 mx-auto mb-4 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                <FolderOpen size={28} className="text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Open Project</h3>
              <p className="text-gray-400 text-sm">Load existing work</p>
            </div>

            <div className="relative">
              <Command className="bg-gray-800/50 border border-gray-600 rounded-xl overflow-hidden">
                <CommandInput 
                  placeholder="Search projects..." 
                  className="bg-transparent text-white placeholder-gray-400 border-0 focus:ring-0 h-12"
                />
                <CommandList className="absolute z-10 w-full bg-gray-800 border border-gray-600 rounded-xl shadow-2xl mt-1 max-h-60 overflow-auto">
                  {projects.length === 0 ? (
                      <CommandEmpty className="text-gray-400 py-8 text-center">No projects found.</CommandEmpty>
                  ) : (
                      <CommandGroup heading="Projects" className="text-gray-300">
                        {projects.map((p) => (
                            <CommandItem
                                key={p}
                                onSelect={() => navigate(`/project/${encodeURIComponent(p)}`)}
                                className="text-white hover:bg-gray-700 cursor-pointer px-4 py-3 transition-colors duration-200"
                            >
                              <FolderOpen className="mr-3 h-4 w-4 text-blue-400" />
                              <span className="truncate">{p}</span>
                            </CommandItem>
                        ))}
                      </CommandGroup>
                  )}
                </CommandList>
              </Command>
            </div>
          </div>
        </div>
      </div>

  );
};

export default LandingPage;
