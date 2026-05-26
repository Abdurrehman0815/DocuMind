import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BrainCircuit, Loader2 } from "lucide-react";
import { cn } from "../utils/cn";
import { supabase } from "../utils/supabaseClient";

type Mode = "login" | "signup";

export default function Auth() {
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const isLogin = mode === "login";

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    if (!isLogin && password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      if (isLogin) {
        const { data, error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (error) throw error;

        if (data.session) {
          localStorage.setItem("token", data.session.access_token);
          navigate("/dashboard");
        }
      } else {
        const { data, error } = await supabase.auth.signUp({
          email,
          password,
        });

        if (error) throw error;

        setMessage("Account created successfully! You can now log in.");
        setMode("login");
        setConfirmPassword("");
      }
    } catch (err: any) {
      setMessage(err.message || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#0a0f1c]">
      {/* Background Orbs */}
      <div className="absolute top-0 left-1/4 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-blue-600/20 blur-[120px]"></div>
      <div className="absolute bottom-0 right-1/4 h-[500px] w-[500px] translate-x-1/2 translate-y-1/2 rounded-full bg-indigo-600/20 blur-[120px]"></div>

      <div className="relative z-10 w-full max-w-md px-4">
        {/* Header */}
        <div className="mb-8 flex flex-col items-center animate-fade-in-up stagger-1">
          <div className="mb-4 rounded-2xl bg-white/5 p-3 shadow-lg ring-1 ring-white/10 backdrop-blur-xl">
            <BrainCircuit className="h-10 w-10 text-primary" />
          </div>
          <div className="text-3xl font-bold text-white mb-2 flex items-center justify-center gap-3">
            <BrainCircuit className="w-8 h-8 text-blue-400" />
            DocuMind
          </div>
          <p className="mt-2 text-center text-sm text-gray-400">
            {isLogin ? "Welcome back" : "Start organizing your life"}
          </p>
        </div>

        {/* Glass Card */}
        <div className="glass-panel overflow-hidden rounded-3xl p-6 sm:p-8 animate-fade-in-up stagger-2 shadow-2xl ring-1 ring-white/10">
          
          {/* Toggle */}
          <div className="relative mb-8 flex h-14 rounded-full bg-black/40 p-1 ring-1 ring-white/10 shadow-inner">
            <div
              className={cn(
                "absolute top-1 bottom-1 w-[calc(50%-4px)] rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 shadow-md transition-all duration-300 ease-out",
                isLogin ? "left-1" : "left-[calc(50%+2px)]"
              )}
            />
            <button
              type="button"
              onClick={() => {
                setMode("login");
                setMessage("");
              }}
              className={cn(
                "relative z-10 flex flex-1 items-center justify-center text-sm font-semibold transition-colors duration-300",
                isLogin ? "text-white" : "text-gray-400 hover:text-white"
              )}
            >
              Login
            </button>
            <button
              type="button"
              onClick={() => {
                setMode("signup");
                setMessage("");
              }}
              className={cn(
                "relative z-10 flex flex-1 items-center justify-center text-sm font-semibold transition-colors duration-300",
                !isLogin ? "text-white" : "text-gray-400 hover:text-white"
              )}
            >
              Signup
            </button>
          </div>

          <h2 className="mb-6 text-center text-2xl font-bold text-white transition-all duration-300">
            {isLogin ? "Login Form" : "Signup Form"}
          </h2>

          <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            <div>
              <input
                className="glass-input transition-all duration-300"
                type="email"
                placeholder="Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <input
                className="glass-input transition-all duration-300"
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
              />
            </div>

            {/* Confirm Password with animated height */}
            <div
              className={cn(
                "overflow-hidden transition-all duration-300 ease-in-out",
                !isLogin ? "max-h-20 opacity-100" : "max-h-0 opacity-0"
              )}
            >
              <input
                className="glass-input"
                type="password"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required={!isLogin}
                minLength={8}
                tabIndex={isLogin ? -1 : 0}
              />
            </div>

            {isLogin && (
              <div className="flex justify-end mt-[-8px]">
                <a href="#" className="text-xs text-primary hover:text-blue-400 transition-colors">
                  Forgot password?
                </a>
              </div>
            )}

            {message && (
              <div className={cn(
                "rounded-lg p-3 text-sm text-center transition-all duration-300",
                message.includes("success") ? "bg-green-500/10 text-green-400 border border-green-500/20" : "bg-red-500/10 text-red-400 border border-red-500/20"
              )}>
                {message}
              </div>
            )}

            <button className="btn-primary mt-2 flex items-center justify-center gap-2" type="submit" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Please wait...
                </>
              ) : (
                isLogin ? "Login" : "Signup"
              )}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-400 transition-all duration-300">
            {isLogin ? "Not a member? " : "Already have an account? "}
            <button
              type="button"
              onClick={() => {
                setMode(isLogin ? "signup" : "login");
                setMessage("");
              }}
              className="font-medium text-primary hover:text-blue-400 transition-colors"
            >
              {isLogin ? "Signup now" : "Login now"}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
