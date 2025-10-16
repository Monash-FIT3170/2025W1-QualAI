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
      <div className="min-h-screen flex flex-col items-center justify-center p-6 space-y-10">
        <div className="text-center space-y-4">
          <h2 className="text-2xl font-light text-gray-400">
            Analyze Interviews with AI
          </h2>

          <div className="w-24 h-24 mx-auto">
            <img
                src="/Logo.png"
                alt="QualAI Logo"
                className="w-full h-full object-cover"
            />
          </div>

          <h1 className="text-5xl font-bold mb-2">QualAI</h1>
          <p className="text-gray-400 text-xl">
            Transcribe and thematically analyze qualitative interview data
          </p>
        </div>

        <div className="flex flex-row gap-8 w-full max-w-2xl">
          <div className="flex-1 bg-white shadow rounded-xl p-6 text-center">
            <h3 className="text-lg font-semibold mb-4">Create New Project</h3>

            <input
                type="text"
                placeholder="Project name"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="px-3 py-2 border rounded w-full mb-4 text-center"
                disabled={loading}
            />

            <button
                onClick={handleCreateProject}
                className={`btn-primary w-full flex items-center justify-center gap-2 ${
                    loading ? "opacity-50 cursor-not-allowed" : ""
                }`}
                disabled={loading}
            >
              <Plus size={20} />
              {loading ? "Creating..." : "Start from scratch"}
            </button>
          </div>

          <div className="flex-1 bg-white shadow rounded-xl p-6">
            <h3 className="text-lg font-semibold mb-4 text-center">Open Project</h3>

            <div className="relative">
              <Command>
                <CommandInput placeholder="Search projects..." />
                <CommandList className="absolute z-10 w-full bg-white border rounded shadow mt-1 max-h-60 overflow-auto">
                  {projects.length === 0 ? (
                      <CommandEmpty>No projects found.</CommandEmpty>
                  ) : (
                      <CommandGroup heading="Projects">
                        {projects.map((p) => (
                            <CommandItem
                                key={p}
                                onSelect={() => navigate(`/project/${encodeURIComponent(p)}`)}
                            >
                              <FolderOpen className="mr-2 h-4 w-4" />
                              {p}
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
