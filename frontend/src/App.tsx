import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Auth from "./pages/Auth";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import ChatPage from "./pages/ChatPage";
import Reminders from "./pages/Reminders";
import Search from "./pages/Search";
import Categories from "./pages/Categories";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/auth" replace />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/login" element={<Navigate to="/auth" replace />} />
        <Route path="/signup" element={<Navigate to="/auth" replace />} />
        
        {/* Protected Routes inside Layout */}
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/reminders" element={<Reminders />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/search" element={<Search />} />
          <Route path="/categories" element={<Categories />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
