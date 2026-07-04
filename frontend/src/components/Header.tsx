import { Bot } from "lucide-react";

export default function Header() {
    return (
        <header className="sticky top-0 z-50 border-b bg-white shadow-sm">
            <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
                <div className="flex items-center gap-3">
                    <div className="rounded-lg bg-blue-600 p-2">
                        <Bot className="h-6 w-6 text-white" />
                    </div>

                    <div>
                        <h1 className="text-xl font-bold text-gray-900">
                            AI Company Research Assistant
                        </h1>

                        <p className="text-sm text-gray-500">
                            Research companies using AI, Serper.dev & OpenRouter
                        </p>
                    </div>
                </div>

                <div className="hidden text-right md:block">
                    <p className="text-sm font-medium text-gray-700">
                        FastAPI + React
                    </p>

                    <p className="text-xs text-gray-500">
                        AI Powered Company Intelligence
                    </p>
                </div>
            </div>
        </header>
    );
}