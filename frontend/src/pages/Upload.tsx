import UploadZone from "../components/UploadZone";

export default function Upload() {
  return (
    <div className="glass-panel rounded-2xl p-6">
      <h3 className="text-lg font-semibold mb-4">Upload New Document</h3>
      <p className="text-sm text-gray-400 mb-6">
        Upload your electricity bills, insurance documents, rent receipts, and more. 
        The AI will automatically classify them and extract important information like due dates and amounts.
      </p>
      <UploadZone onUploadSuccess={() => {
        alert("Upload successful! The AI is now analyzing your document in the background.");
      }} />
    </div>
  );
}
