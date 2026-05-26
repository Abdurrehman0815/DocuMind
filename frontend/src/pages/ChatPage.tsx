import ChatInterface from "../components/ChatInterface";

export default function ChatPage() {
  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div className="mb-6">
        <h2 className="text-2xl font-bold">AI Assistant</h2>
        <p className="text-gray-400 mt-2">
          Ask questions about your uploaded documents. The AI uses semantic search to find the exact paragraphs needed to answer your questions.
        </p>
      </div>
      <div className="flex-1 min-h-0">
        <ChatInterface />
      </div>
    </div>
  );
}
