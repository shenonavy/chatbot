import { ChatType } from "@/enum";
import { useChat } from "@/hook/use-chat";
import { IChatResponse } from "@/models";

export default function Home() {
  const { input, chats, isLoading, setInput, onSubmit } = useChat();

  return (
    <div className="bg-gray-100 h-screen flex flex-col">
      <div className="bg-blue-600 text-white p-4 text-lg font-semibold">
        Chatbot Assistant
      </div>

      <div id="chat-window" className="flex-1 overflow-y-auto p-4 space-y-4">
        {chats?.map((chat: IChatResponse, index: number) => (
          <div
            key={index}
            className={`flex ${
              chat.type === ChatType.Agent ? "justify-start" : "justify-end"
            }`}
          >
            <div
              className={`p-3 rounded-lg max-w-xs ${
                chat.type === ChatType.Agent
                  ? "bg-gray-200 text-gray-900"
                  : "bg-blue-500 text-white"
              }`}
            >
              {chat.response}
            </div>
          </div>
        ))}

        {isLoading && (
          <div
            id="typing-indicator"
            className="flex justify-start items-center space-x-2"
          >
            <span className="ml-1 text-sm text-gray-500">Bot is typing...</span>
          </div>
        )}
      </div>

      <div className="p-4 bg-white flex items-center space-x-2">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300"
          value={input}
          onInput={(e) => setInput(e.currentTarget.value)}
        />
        <button
          disabled={isLoading}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          onClick={() => onSubmit()}
        >
          Send
        </button>
      </div>
    </div>
  );
}
