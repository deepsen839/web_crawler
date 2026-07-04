import { useEffect, useState } from "react";
import { Save, Bot } from "lucide-react";

export interface DiscordConfig {
    botToken: string;
    channelId: string;
    applicantName: string;
    applicantEmail: string;
}

interface Props {
    onSave: (config: DiscordConfig) => void;
}

export default function DiscordSettings({ onSave }: Props) {
    const [botToken, setBotToken] = useState("");
    const [channelId, setChannelId] = useState("");
    const [applicantName, setApplicantName] = useState("");
    const [applicantEmail, setApplicantEmail] = useState("");

    useEffect(() => {
        const saved = localStorage.getItem("discord-config");

        if (!saved) return;

        try {
            const config: DiscordConfig = JSON.parse(saved);

            setBotToken(config.botToken);
            setChannelId(config.channelId);
            setApplicantName(config.applicantName);
            setApplicantEmail(config.applicantEmail);

            onSave(config);
        } catch {
            console.error("Failed to load Discord configuration.");
        }
    }, [onSave]);

    const handleSave = () => {
        const config: DiscordConfig = {
            botToken,
            channelId,
            applicantName,
            applicantEmail,
        };

        localStorage.setItem(
            "discord-config",
            JSON.stringify(config)
        );

        onSave(config);

        alert("Configuration saved successfully.");
    };

    return (
        <div className="mb-8 rounded-xl bg-white p-6 shadow-lg">

            <div className="mb-6 flex items-center gap-3">

                <Bot
                    className="text-blue-600"
                    size={28}
                />

                <div>

                    <h2 className="text-xl font-bold">
                        Discord Integration
                    </h2>

                    <p className="text-sm text-gray-500">
                        Configure Discord settings for automatic report delivery.
                    </p>

                </div>

            </div>

            <div className="grid gap-5 md:grid-cols-2">

                <div>

                    <label className="mb-2 block text-sm font-semibold">
                        Discord Bot Token
                    </label>

                    <input
                        type="password"
                        value={botToken}
                        onChange={(e) =>
                            setBotToken(e.target.value)
                        }
                        placeholder="Discord Bot Token"
                        className="w-full rounded-lg border px-4 py-3"
                    />

                </div>

                <div>

                    <label className="mb-2 block text-sm font-semibold">
                        Discord Channel ID
                    </label>

                    <input
                        type="text"
                        value={channelId}
                        onChange={(e) =>
                            setChannelId(e.target.value)
                        }
                        placeholder="Discord Channel ID"
                        className="w-full rounded-lg border px-4 py-3"
                    />

                </div>

                <div>

                    <label className="mb-2 block text-sm font-semibold">
                        Applicant Name
                    </label>

                    <input
                        type="text"
                        value={applicantName}
                        onChange={(e) =>
                            setApplicantName(e.target.value)
                        }
                        placeholder="Applicant Name"
                        className="w-full rounded-lg border px-4 py-3"
                    />

                </div>

                <div>

                    <label className="mb-2 block text-sm font-semibold">
                        Applicant Email
                    </label>

                    <input
                        type="email"
                        value={applicantEmail}
                        onChange={(e) =>
                            setApplicantEmail(e.target.value)
                        }
                        placeholder="Applicant Email"
                        className="w-full rounded-lg border px-4 py-3"
                    />

                </div>

            </div>

            <div className="mt-6">

                <button
                    onClick={handleSave}
                    className="flex items-center gap-2 rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
                >
                    <Save size={18} />

                    Save Configuration

                </button>

            </div>

        </div>
    );
}