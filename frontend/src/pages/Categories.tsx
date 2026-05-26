import { useEffect, useState } from "react";
import { Folder, FileText, Image as ImageIcon, Eye } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface Document {
  id: number;
  filename: string;
  file_path: string;
  content_type: string;
  category: string;
  created_at: string;
}

export default function Categories() {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return navigate("/auth");
        
        const response = await fetch("/api/v1/upload", {
          headers: { "Authorization": `Bearer ${token}` }
        });
        
        if (response.ok) {
          const data = await response.json();
          setDocuments(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDocuments();
  }, [navigate]);

  const formatDate = (dateString: string) => {
    const d = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(d);
  };

  // Group by category
  const grouped = documents.reduce((acc, doc) => {
    const cat = doc.category || "Uncategorized";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(doc);
    return acc;
  }, {} as Record<string, Document[]>);
  
  // Sort categories alphabetically
  const sortedCategories = Object.keys(grouped).sort();

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-blue-500/20 rounded-xl">
          <Folder className="h-6 w-6 text-blue-400" />
        </div>
        <div>
          <h2 className="text-2xl font-bold">Categorized Documents</h2>
          <p className="text-gray-400">Your documents organized by AI classification.</p>
        </div>
      </div>

      {loading ? (
        <div className="glass-panel rounded-2xl p-8 text-center text-gray-400">
          Loading documents...
        </div>
      ) : documents.length === 0 ? (
        <div className="glass-panel rounded-2xl p-12 text-center flex flex-col items-center">
          <FileText className="h-12 w-12 text-gray-500 mb-4 opacity-50" />
          <h3 className="text-lg font-medium text-white mb-2">No documents found</h3>
          <p className="text-gray-400 max-w-md mb-6">
            Upload documents to see them automatically categorized here.
          </p>
          <button onClick={() => navigate("/upload")} className="px-6 py-2 bg-blue-600 rounded-lg text-white font-medium hover:bg-blue-500">
            Go to Upload Center
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {sortedCategories.map(category => (
            <div key={category} className="glass-panel rounded-2xl p-6">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                {category}
                <span className="text-xs font-normal text-gray-400 bg-white/10 px-2 py-0.5 rounded-full">
                  {grouped[category].length}
                </span>
              </h3>
              
              <div className="space-y-3">
                {grouped[category].map(doc => (
                  <div key={doc.id} className="flex items-center justify-between p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-colors border border-transparent hover:border-white/10 group">
                    <div className="flex items-center gap-3 overflow-hidden">
                      <div className="text-gray-400 flex-shrink-0">
                        {doc.content_type?.startsWith("image/") ? <ImageIcon className="h-4 w-4" /> : <FileText className="h-4 w-4" />}
                      </div>
                      <div className="truncate">
                        <p className="text-sm text-gray-200 truncate pr-2">{doc.filename}</p>
                        <p className="text-[10px] text-gray-500">{formatDate(doc.created_at)}</p>
                      </div>
                    </div>
                    <a 
                      href={doc.file_path || "#"} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="p-2 text-gray-400 hover:text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Eye className="h-4 w-4" />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
