import { useState } from "react";
import { Search as SearchIcon, FileText, Image as ImageIcon, Eye, Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface SearchResult {
  id: number;
  filename: string;
  file_path: string;
  content_type: string;
  category: string;
  created_at: string;
  matching_chunk: string;
}

export default function Search() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setHasSearched(true);
    
    try {
      const token = localStorage.getItem("token");
      if (!token) return navigate("/auth");
      
      const response = await fetch(`/api/v1/search?q=${encodeURIComponent(query)}`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const d = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(d);
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col items-center justify-center pt-8 pb-4">
        <div className="p-4 bg-blue-500/10 rounded-2xl mb-6">
          <SearchIcon className="h-10 w-10 text-blue-400" />
        </div>
        <h2 className="text-3xl font-bold mb-3">Semantic Search</h2>
        <p className="text-gray-400 text-center max-w-lg mb-8">
          Search by meaning, not just keywords. Try asking: "Show unpaid bills", "Find insurance documents", or "Which documents expire next month?"
        </p>

        <form onSubmit={handleSearch} className="w-full max-w-2xl relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type your search query..."
            className="w-full bg-white/5 border border-white/10 rounded-full pl-6 pr-16 py-4 text-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/50 shadow-2xl transition-all"
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-3 rounded-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 transition-colors text-white"
          >
            {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <SearchIcon className="h-5 w-5" />}
          </button>
        </form>
      </div>

      {hasSearched && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
            Results <span className="text-sm font-normal text-gray-400 bg-white/10 px-2 py-0.5 rounded-full">{results.length}</span>
          </h3>

          {loading ? (
            <div className="grid grid-cols-1 gap-4">
              {[1, 2, 3].map(i => (
                <div key={i} className="glass-panel rounded-2xl p-6 h-32 animate-pulse flex flex-col justify-center gap-4">
                  <div className="h-4 bg-white/10 rounded w-1/4"></div>
                  <div className="h-3 bg-white/10 rounded w-3/4"></div>
                  <div className="h-3 bg-white/10 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : results.length === 0 ? (
            <div className="glass-panel rounded-2xl p-12 text-center text-gray-400">
              No documents matched your search conceptually.
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-6">
              {results.map((result) => (
                <div key={result.id} className="glass-panel rounded-2xl p-6 border border-white/5 hover:border-blue-500/30 transition-all hover:bg-white/5 group">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div className="flex items-center gap-3 min-w-0 flex-1">
                      <div className="p-2.5 rounded-xl bg-blue-500/10 text-blue-400 flex-shrink-0">
                        {result.content_type?.startsWith("image/") ? <ImageIcon className="h-5 w-5" /> : <FileText className="h-5 w-5" />}
                      </div>
                      <div className="min-w-0 flex-1">
                        <h4 className="text-lg font-bold text-white group-hover:text-blue-400 transition-colors truncate">{result.filename}</h4>
                        <div className="flex items-center gap-3 mt-1 text-xs text-gray-400 truncate">
                          <span className="flex-shrink-0">{formatDate(result.created_at)}</span>
                          {result.category && (
                            <span className="px-2 py-0.5 rounded-full bg-white/10 text-white font-medium truncate">
                              {result.category}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                    <a 
                      href={result.file_path || "#"} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="p-2.5 text-blue-400 hover:bg-blue-400/10 rounded-xl transition-colors bg-blue-500/5"
                      title="View Document"
                    >
                      <Eye className="h-4 w-4" />
                    </a>
                  </div>
                  
                  {result.matching_chunk && (
                    <div className="mt-4 p-4 rounded-xl bg-[#0a0f1c]/50 border border-white/5 relative">
                      <div className="absolute -top-3 left-4 bg-[#0a0f1c] px-2 text-[10px] uppercase tracking-wider font-bold text-blue-400">
                        Relevant Excerpt
                      </div>
                      <p className="text-sm text-gray-300 leading-relaxed italic">
                        "...{result.matching_chunk.substring(0, 300)}{result.matching_chunk.length > 300 ? "..." : ""}..."
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
