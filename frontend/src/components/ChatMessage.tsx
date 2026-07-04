import { Bot, User } from "lucide-react";

interface ChatMessageProps {
    role: "user" | "assistant";
    message: string;
}

export default function ChatMessage({
    role,
    message,
}: ChatMessageProps) {
    const isUser = role === "user";

    return (
        <div
            className={`flex ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >
            <div
                className={`flex max-w-3xl gap-3 ${
                    isUser ? "flex-row-reverse" : ""
                }`}
            >
                {/* Avatar */}
                <div
                    className={`flex h-10 w-10 items-center justify-center rounded-full ${
                        isUser
                            ? "bg-blue-600 text-white"
                            : "bg-gray-800 text-white"
                    }`}
                >
                    {isUser ? (
                        <User size={20} />
                    ) : (
                        <Bot size={20} />
                    )}
                </div>

                {/* Bubble */}
                <div
                    className={`rounded-2xl px-5 py-4 shadow ${
                        isUser
                            ? "bg-blue-600 text-white"
                            : "bg-white text-gray-900"
                    }`}
                >
                    <p className="whitespace-pre-wrap break-words">
                        {message}
                    </p>
                </div>
            </div>
        </div>
    );
}