import { useEffect, useState } from "react";
import { FileText, Image as ImageIcon, Eye, Trash2, Bell, Clock, Wand2, X, Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface Document {
  id: number;
  filename: string;
  file_path: string;
  content_type: string;
  status: string;
  created_at: string;
}

interface Reminder {
  id: number;
  document_id: number;
  filename: string;
  category: string;
  date: string;
  type: string;
  amount?: string;
  provider?: string;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [summaryModalOpen, setSummaryModalOpen] = useState(false);
  const [selectedSummary, setSelectedSummary] = useState("");
  const [isSummarizing, setIsSummarizing] = useState<number | null>(null);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/auth");
        return;
      }
      
      const headers = { "Authorization": `Bearer ${token}` };
      
      const [docsRes, remindersRes] = await Promise.all([
        fetch("/api/v1/upload", { headers }),
        fetch("/api/v1/reminders", { headers })
      ]);
      
      if (docsRes.ok) {
        const data = await docsRes.json();
        setDocuments(data);
      } else if (docsRes.status === 401) {
        localStorage.removeItem("token");
        navigate("/auth");
      }
      
      if (remindersRes.ok) {
        const data = await remindersRes.json();
        setReminders(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this document?")) return;
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`/api/v1/upload/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (response.ok) fetchDashboardData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSummarize = async (id: number) => {
    setIsSummarizing(id);
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`/api/v1/upload/${id}/summarize`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setSelectedSummary(data.summary);
        setSummaryModalOpen(true);
      } else {
        alert("Failed to summarize. Make sure the document text has been extracted.");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsSummarizing(null);
    }
  };

  const formatDate = (dateString: string) => {
    const d = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(d);
  };
  
  const getUrgencyText = (dateString: string) => {
    const timeDiff = new Date(dateString).getTime() - new Date().getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
    
    if (daysDiff < 0) return `Overdue by ${Math.abs(daysDiff)} days`;
    if (daysDiff === 0) return "Due Today";
    if (daysDiff === 1) return "Due Tomorrow";
    return `Due in ${daysDiff} days`;
  };

  const getUrgencyColor = (dateString: string) => {
    const timeDiff = new Date(dateString).getTime() - new Date().getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
    if (daysDiff < 0) return "text-red-400";
    if (daysDiff <= 7) return "text-amber-400";
    return "text-green-400";
  };

  return (
    <>
      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="glass-panel rounded-2xl p-6">
          <h3 className="text-sm font-medium text-gray-400">Total Documents</h3>
          <p className="mt-2 text-3xl font-bold">{loading ? "..." : documents.length}</p>
        </div>
        
        {/* Reminders Widget */}
        <div className="glass-panel rounded-2xl p-6 md:col-span-2 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-400 flex items-center gap-2">
              <Bell className="h-4 w-4" /> Upcoming Deadlines
            </h3>
            <button onClick={() => navigate("/reminders")} className="text-xs text-blue-400 hover:text-blue-300 font-medium">View All</button>
          </div>
          
          {loading ? (
            <p className="text-gray-500 text-sm">Loading...</p>
          ) : reminders.length === 0 ? (
            <p className="text-gray-500 text-sm italic">No upcoming deadlines found in your documents.</p>
          ) : (
            <div className="space-y-3">
              {reminders.slice(0, 2).map(r => (
                <div key={r.id} className="flex items-center justify-between bg-white/5 rounded-lg px-4 py-2 border border-white/5">
                  <div className="flex items-center gap-3">
                    <Clock className={`h-4 w-4 ${getUrgencyColor(r.date)}`} />
                    <span className="text-sm font-medium">{r.provider || r.category || "Document"}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-bold">{r.amount || ""}</span>
                    <span className={`text-xs font-semibold px-2 py-1 bg-white/5 rounded-md ${getUrgencyColor(r.date)}`}>
                      {getUrgencyText(r.date)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Document List */}
      <div className="glass-panel rounded-2xl p-6 h-full min-h-[400px]">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold">Your Documents</h3>
          <button onClick={() => navigate("/categories")} className="text-sm text-blue-400 hover:text-blue-300 font-medium">View All Categories</button>
        </div>

        {loading ? (
          <div className="flex h-40 items-center justify-center text-gray-400">Loading documents...</div>
        ) : documents.length === 0 ? (
          <div className="flex h-40 flex-col items-center justify-center text-gray-400 border border-dashed border-white/10 rounded-xl bg-white/5">
            <FileText className="h-8 w-8 mb-2 opacity-50" />
            <p className="text-sm">No documents uploaded yet.</p>
            <button onClick={() => navigate("/upload")} className="mt-4 px-4 py-2 bg-blue-600 rounded-lg text-white text-sm hover:bg-blue-500">Go to Upload Center</button>
          </div>
        ) : (
          <div className="space-y-3">
            {documents.slice(0, 10).map((doc) => (
              <div key={doc.id} className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors group">
                <div className="flex items-center gap-4 overflow-hidden">
                  <div className="p-2.5 rounded-lg bg-blue-500/10 text-blue-400 flex-shrink-0">
                    {doc.content_type.startsWith("image/") ? <ImageIcon className="h-5 w-5" /> : <FileText className="h-5 w-5" />}
                  </div>
                  <div className="truncate">
                    <p className="text-sm font-medium text-white truncate pr-4">{doc.filename}</p>
                    <p className="text-xs text-gray-400 mt-0.5">{formatDate(doc.created_at)}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="px-2.5 py-1 rounded-full bg-green-500/10 text-green-400 text-[10px] font-semibold uppercase tracking-wider hidden sm:inline-block">
                    {doc.status}
                  </span>
                  
                  {/* Action Buttons */}
                  <div className="flex items-center gap-1 opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity">
                    <button 
                      onClick={() => handleSummarize(doc.id)}
                      disabled={isSummarizing === doc.id}
                      className="p-2 text-gray-400 hover:text-purple-400 hover:bg-purple-400/10 rounded-lg transition-colors disabled:opacity-50"
                      title="AI Summarize"
                    >
                      {isSummarizing === doc.id ? <Loader2 className="h-4 w-4 animate-spin text-purple-400" /> : <Wand2 className="h-4 w-4" />}
                    </button>
                    <a 
                      href={doc.file_path || "#"} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="p-2 text-gray-400 hover:text-blue-400 hover:bg-blue-400/10 rounded-lg transition-colors"
                      title="View Document"
                    >
                      <Eye className="h-4 w-4" />
                    </a>
                    <button 
                      onClick={() => handleDelete(doc.id)}
                      className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors"
                      title="Delete Document"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Summary Modal */}
      {summaryModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="glass-panel w-full max-w-2xl rounded-2xl overflow-hidden shadow-2xl border border-white/20 animate-in fade-in zoom-in duration-200">
            <div className="flex items-center justify-between p-6 border-b border-white/10 bg-white/5">
              <h3 className="text-xl font-bold flex items-center gap-2">
                <Wand2 className="h-5 w-5 text-purple-400" /> AI Document Summary
              </h3>
              <button 
                onClick={() => setSummaryModalOpen(false)}
                className="p-2 text-gray-400 hover:text-white rounded-lg transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="p-8 max-h-[70vh] overflow-y-auto">
              <div className="prose prose-invert max-w-none text-gray-300">
                {selectedSummary.split('\n').map((line, i) => (
                  <p key={i} className={line.startsWith('-') ? "ml-4" : ""}>
                    {line}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
