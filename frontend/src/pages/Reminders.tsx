import { useEffect, useState } from "react";
import { Bell, Calendar, Clock, AlertTriangle } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface Reminder {
  id: number;
  document_id: number;
  filename: string;
  category: string;
  date: string;
  type: string;
  amount?: string;
  provider?: string;
  priority: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
}

export default function Reminders() {
  const navigate = useNavigate();
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReminders = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return navigate("/auth");
        
        const response = await fetch("/api/v1/reminders", {
          headers: { "Authorization": `Bearer ${token}` }
        });
        
        if (response.ok) {
          const data = await response.json();
          setReminders(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchReminders();
  }, [navigate]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
    });
  };

  const getUrgencyColor = (priority: string) => {
    if (priority === "CRITICAL") return "text-red-400 bg-red-400/10 border-red-400/20";
    if (priority === "HIGH") return "text-amber-400 bg-amber-400/10 border-amber-400/20";
    if (priority === "MEDIUM") return "text-blue-400 bg-blue-400/10 border-blue-400/20";
    return "text-green-400 bg-green-400/10 border-green-400/20";
  };

  const getUrgencyText = (dateString: string) => {
    const timeDiff = new Date(dateString).getTime() - new Date().getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
    
    if (daysDiff < 0) return `Overdue by ${Math.abs(daysDiff)} days`;
    if (daysDiff === 0) return "Due Today";
    if (daysDiff === 1) return "Due Tomorrow";
    return `Due in ${daysDiff} days`;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-blue-500/20 rounded-xl">
          <Bell className="h-6 w-6 text-blue-400" />
        </div>
        <div>
          <h2 className="text-2xl font-bold">Smart Reminders</h2>
          <p className="text-gray-400">Deadlines automatically extracted from your documents by AI.</p>
        </div>
      </div>

      {loading ? (
        <div className="glass-panel rounded-2xl p-8 text-center text-gray-400">
          Loading reminders...
        </div>
      ) : reminders.length === 0 ? (
        <div className="glass-panel rounded-2xl p-12 text-center flex flex-col items-center">
          <Calendar className="h-12 w-12 text-gray-500 mb-4 opacity-50" />
          <h3 className="text-lg font-medium text-white mb-2">No upcoming deadlines</h3>
          <p className="text-gray-400 max-w-md">
            We haven't found any due dates or expiry dates in your uploaded documents. 
            Upload a bill or insurance policy to see this in action.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {reminders.map((reminder) => {
            const urgencyClass = getUrgencyColor(reminder.priority);
            
            return (
              <div key={reminder.id} className={`glass-panel rounded-2xl p-6 border ${urgencyClass.split(' ')[2]}`}>
                <div className="flex justify-between items-start mb-4 gap-4">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 mb-3 flex-wrap">
                      <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold tracking-wider ${urgencyClass.split(' ').slice(0, 2).join(' ')}`}>
                        {reminder.priority}
                      </span>
                      <span className="text-sm text-gray-400 font-medium whitespace-nowrap">
                        {getUrgencyText(reminder.date)}
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-white truncate">{reminder.provider || reminder.filename || reminder.category || "Document"}</h3>
                    <p className="text-sm text-gray-400 flex items-center gap-1 mt-1 truncate">
                      <Clock className="h-3 w-3 flex-shrink-0" />
                      <span className="truncate">{formatDate(reminder.date)}</span>
                    </p>
                  </div>
                  {reminder.amount && (
                    <div className="text-right flex-shrink-0">
                      <span className="text-2xl font-bold text-white">{reminder.amount}</span>
                    </div>
                  )}
                </div>
                
                <div className="mt-4 pt-4 border-t border-white/10 flex justify-between items-center">
                  <span className="text-sm text-gray-400 truncate pr-4 text-xs">
                    Source: {reminder.filename}
                  </span>
                  <button className="text-sm text-blue-400 hover:text-blue-300 font-medium whitespace-nowrap bg-blue-500/10 px-3 py-1.5 rounded-lg transition-colors">
                    Pay Now
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
