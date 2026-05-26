import { useState, useRef, useEffect } from "react";
import { Upload as UploadIcon, File as FileIcon, CheckCircle2, Loader2, AlertCircle, FileText } from "lucide-react";
import { cn } from "../utils/cn";

interface UploadZoneProps {
  onUploadSuccess?: (data: any) => void;
}

export default function UploadZone({ onUploadSuccess }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!file) {
      setPreview(null);
      return;
    }

    if (file.type.startsWith("image/")) {
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);
      return () => URL.revokeObjectURL(objectUrl);
    } else {
      setPreview(null);
    }
  }, [file]);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const validateAndSetFile = (selectedFile: File) => {
    const validTypes = ["application/pdf", "image/png", "image/jpeg", "image/jpg"];
    if (!validTypes.includes(selectedFile.type)) {
      setStatus("error");
      setErrorMessage("Only PDF, PNG, and JPG files are supported.");
      return;
    }
    
    if (selectedFile.size > 10 * 1024 * 1024) {
      setStatus("error");
      setErrorMessage("File size exceeds 10MB limit.");
      return;
    }

    setFile(selectedFile);
    setStatus("idle");
    setErrorMessage("");
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setProgress(0);
    setStatus("idle");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const interval = setInterval(() => {
        setProgress((prev) => (prev >= 90 ? 90 : prev + 15));
      }, 150);

      // Add a small artificial delay so the user actually sees the upload UI before it completes instantly on localhost
      await new Promise(resolve => setTimeout(resolve, 800));

      const token = localStorage.getItem("token");
      const headers: HeadersInit = {};
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch("/api/v1/upload", {
        method: "POST",
        body: formData,
        headers,
      });

      clearInterval(interval);
      setProgress(100);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setStatus("success");
      if (onUploadSuccess) onUploadSuccess(data);
      
      setTimeout(() => {
        setFile(null);
        setStatus("idle");
        setProgress(0);
      }, 3000);
      
    } catch (err: any) {
      setStatus("error");
      setErrorMessage(err.message || "An error occurred during upload.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="w-full">
      <div
        className={cn(
          "relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-8 text-center transition-all duration-200",
          isDragging
            ? "border-primary bg-primary/10"
            : "border-white/20 bg-white/5 hover:border-white/40 hover:bg-white/10",
          file ? "border-solid border-white/20" : ""
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          className="hidden"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.png,.jpg,.jpeg"
        />

        {!file ? (
          <>
            <div className="mb-4 rounded-full bg-white/5 p-4 shadow-inner ring-1 ring-white/10">
              <UploadIcon className="h-8 w-8 text-primary" />
            </div>
            <h2 className="mb-2 text-xl font-semibold">Upload your document</h2>
            <p className="mb-6 max-w-md text-sm text-muted-foreground">
              Drag and drop your bills, insurance documents, or receipts here. Supported formats: PDF, PNG, JPG.
            </p>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="btn-secondary"
            >
              Browse Files
            </button>
          </>
        ) : (
          <div className="flex w-full flex-col items-center">
            {preview ? (
              <div className="mb-4 h-32 w-32 overflow-hidden rounded-xl ring-2 ring-white/20 shadow-lg">
                <img src={preview} alt="Preview" className="h-full w-full object-cover" />
              </div>
            ) : (
              <div className="mb-4 flex h-32 w-32 items-center justify-center rounded-xl bg-blue-500/10 ring-2 ring-blue-500/20 shadow-lg">
                <FileText className="h-12 w-12 text-blue-400" />
              </div>
            )}
            
            <p className="mb-1 max-w-xs truncate font-medium">{file.name}</p>
            <p className="mb-6 text-xs text-muted-foreground">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>

            {uploading && (
              <div className="mb-6 w-full max-w-xs">
                <div className="mb-2 flex justify-between text-xs">
                  <span>Uploading...</span>
                  <span>{progress}%</span>
                </div>
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-white/10">
                  <div
                    className="h-full bg-primary transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            )}

            {status === "error" && (
              <div className="mb-4 flex items-center gap-2 rounded-lg bg-red-500/10 px-4 py-2 text-sm text-red-400 ring-1 ring-red-500/20">
                <AlertCircle className="h-4 w-4" />
                {errorMessage}
              </div>
            )}

            {status === "success" && (
              <div className="mb-4 flex items-center gap-2 rounded-lg bg-green-500/10 px-4 py-2 text-sm text-green-400 ring-1 ring-green-500/20">
                <CheckCircle2 className="h-4 w-4" />
                Upload complete!
              </div>
            )}

            <div className="flex gap-3">
              {!uploading && status !== "success" && (
                <button
                  onClick={() => setFile(null)}
                  className="rounded-xl border border-white/10 bg-transparent px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-white/5"
                >
                  Cancel
                </button>
              )}
              {!uploading && status !== "success" && (
                <button onClick={handleUpload} className="btn-primary px-6 py-2">
                  Confirm Upload
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
