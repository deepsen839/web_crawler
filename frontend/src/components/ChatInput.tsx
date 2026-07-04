import { useState } from "react";
import { Send } from "lucide-react";

interface Props {
    onSubmit: (
        company: string,
        applicantName: string,
        applicantEmail: string,
        model: string
    ) => void;
}

const MODELS = [
    "google/gemini-2.5-pro",
    "openai/gpt-oss-20b:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen3-235b-a22b",
    "deepseek/deepseek-chat-v3",
];

export default function ChatInput({ onSubmit }: Props) {
    const [company, setCompany] = useState("");

    const [applicantName, setApplicantName] = useState("");

    const [applicantEmail, setApplicantEmail] = useState("");

    const [model, setModel] = useState(MODELS[0]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!company.trim()) return;

        onSubmit(
            company.trim(),
            applicantName.trim(),
            applicantEmail.trim(),
            model
        );

        setCompany("");
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="rounded-xl bg-white shadow-md p-6 space-y-5"
        >
            <div>
                <label className="block text-sm font-semibold mb-2">
                    Company Name or Website
                </label>

                <input
                    type="text"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    placeholder="Microsoft or https://stripe.com"
                    className="w-full rounded-lg border px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

            <div className="grid md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-semibold mb-2">
                        Applicant Name
                    </label>

                    <input
                        type="text"
                        value={applicantName}
                        onChange={(e) =>
                            setApplicantName(e.target.value)
                        }
                        placeholder="John Doe"
                        className="w-full rounded-lg border px-4 py-3"
                    />
                </div>

                <div>
                    <label className="block text-sm font-semibold mb-2">
                        Applicant Email
                    </label>

                    <input
                        type="email"
                        value={applicantEmail}
                        onChange={(e) =>
                            setApplicantEmail(e.target.value)
                        }
                        placeholder="john@example.com"
                        className="w-full rounded-lg border px-4 py-3"
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-semibold mb-2">
                    OpenRouter Model
                </label>

                <select
                    value={model}
                    onChange={(e) => setModel(e.target.value)}
                    className="w-full rounded-lg border px-4 py-3"
                >
                    {MODELS.map((item) => (
                        <option
                            key={item}
                            value={item}
                        >
                            {item}
                        </option>
                    ))}
                </select>
            </div>

            <button
                type="submit"
                className="flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700"
            >
                <Send size={18} />

                Research Company
            </button>
        </form>
    );
}