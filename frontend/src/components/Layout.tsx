import { useState, useEffect } from "react";
import { useNavigate, useLocation, Outlet } from "react-router-dom";
import { LogOut, LayoutDashboard, Upload, Bell, Search, FileText, Bot, Menu, X } from "lucide-react";
import { supabase } from "../utils/supabaseClient";

export default function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location.pathname]);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    localStorage.removeItem("token");
    navigate("/auth");
  };

  const navItems = [
    { name: "Document Overview", path: "/dashboard", icon: LayoutDashboard },
    { name: "Upload Center", path: "/upload", icon: Upload },
    { name: "Reminders Section", path: "/reminders", icon: Bell },
    { name: "AI Assistant", path: "/chat", icon: Bot },
    { name: "Semantic Search", path: "/search", icon: Search },
    { name: "Categorized Documents", path: "/categories", icon: FileText },
  ];

  return (
    <div className="flex h-screen bg-[#0a0f1c] text-white overflow-hidden">
      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`fixed md:relative w-64 h-full border-r border-white/10 bg-[#0a0f1c]/95 md:bg-white/5 backdrop-blur-xl flex flex-col z-50 transition-transform duration-300 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        <div className="flex items-center gap-3 mb-8 px-2">
          <div className="p-2 bg-blue-500/20 rounded-xl">
            <FileText className="h-6 w-6 text-blue-400" />
          </div>
          <span className="text-lg font-bold tracking-wide">DocuMind</span>
        </div>

        <nav className="flex-1 space-y-1 p-4">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive 
                    ? "bg-blue-600/10 text-blue-400" 
                    : "text-gray-400 hover:bg-white/5 hover:text-white"
                }`}
              >
                <Icon className="h-4 w-4" />
                {item.name}
              </button>
            );
          })}
        </nav>

        <div className="border-t border-white/10 p-4">
          <button 
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-red-400 hover:bg-red-400/10 transition-colors"
          >
            <LogOut className="h-4 w-4" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content Wrapper */}
      <main className="flex-1 flex flex-col relative overflow-y-auto">
        {/* Top Header */}
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-white/10 bg-[#0a0f1c]/80 px-4 md:px-8 backdrop-blur-xl">
          <div className="flex items-center gap-4">
            <button 
              className="md:hidden p-2 -ml-2 text-gray-400 hover:text-white"
              onClick={() => setIsMobileMenuOpen(true)}
            >
              <Menu className="h-6 w-6" />
            </button>
            <h1 className="text-lg font-semibold truncate max-w-[200px] md:max-w-none">
              {navItems.find(item => item.path === location.pathname)?.name || "Overview"}
            </h1>
          </div>
          <div className="flex items-center gap-2 md:gap-4">
            <div className="relative hidden sm:block">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input 
                type="text" 
                placeholder="Ask AI or search..." 
                className="h-9 w-48 md:w-64 rounded-full border border-white/10 bg-white/5 pl-9 pr-4 text-sm outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all text-white placeholder-gray-500"
                onClick={() => navigate("/search")}
              />
            </div>
            <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center font-bold text-xs shadow-lg">
              AR
            </div>
          </div>
        </header>

        {/* Page Content Rendered Here */}
        <div className="p-4 md:p-8 max-w-6xl mx-auto w-full">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
