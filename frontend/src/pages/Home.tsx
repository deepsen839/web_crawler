import { useState } from "react";

import Header from "@/components/Header";
import ChatInput from "@/components/ChatInput";
import ChatMessage from "@/components/ChatMessage";
import CompanyCard from "@/components/CompanyCard";
import CompetitorCard from "@/components/CompetitorCard";
import Loader from "@/components/Loader";
import DiscordSettings from "@/components/DiscordSettings";
import type { DiscordConfig } from "@/components/DiscordSettings";

import api from "@/api/api";

import type { ResearchResponse } from "@/types/company";
interface ChatMessageData {
    role: "user" | "assistant";
    content?: string;
    data?: ResearchResponse;
    error?: string;
}

export default function Home() {
    const [messages, setMessages] = useState<ChatMessageData[]>([]);

    const [loading, setLoading] = useState(false);

    const [discordConfig, setDiscordConfig] =
        useState<DiscordConfig | null>(null);

    const sendMessage = async (
        company: string,
        applicantName: string,
        applicantEmail: string,
        model: string
    ) => {
        setLoading(true);

        setMessages((prev) => [
            ...prev,
            {
                role: "user",
                content: company,
            },
        ]);

        try {
            const { data } = await api.post("/research", {
                company,

                // Applicant details
                applicant_name:
                    discordConfig?.applicantName || applicantName,

                applicant_email:
                    discordConfig?.applicantEmail || applicantEmail,

                // Discord configuration
                discord_bot_token:
                    discordConfig?.botToken ?? "",

                discord_channel_id:
                    discordConfig?.channelId ?? "",

                // Selected AI Model
                model,
            });

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    data,
                },
            ]);
        } catch (err: any) {
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    error:
                        err?.response?.data?.detail ??
                        "Something went wrong.",
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <Header />

            <div className="mx-auto max-w-7xl px-6 py-8">

                <DiscordSettings
                    onSave={setDiscordConfig}
                />

                <ChatInput
                    onSubmit={sendMessage}
                />

                <div className="mt-8 space-y-6">

                    {messages.map((message, index) => (
                        <div key={index}>

                            {message.role === "user" && (
                                <ChatMessage
                                    role="user"
                                    message={message.content ?? ""}
                                />
                            )}

                            {message.role === "assistant" &&
                                message.data && (
                                    <>
                                        <CompanyCard
                                            company={message.data.company}
                                            downloadUrl={
                                                message.data.download_url
                                            }
                                        />

                                        <CompetitorCard
                                            competitors={
                                                message.data.competitors
                                            }
                                        />
                                    </>
                                )}

                            {message.role === "assistant" &&
                                message.error && (
                                    <ChatMessage
                                        role="assistant"
                                        message={message.error}
                                    />
                                )}

                        </div>
                    ))}

                    {loading && <Loader />}

                </div>
            </div>
        </div>
    );
}