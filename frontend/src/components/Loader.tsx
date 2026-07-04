import { useEffect, useState } from "react";
import { Loader2 } from "lucide-react";

const STEPS = [
    "🔍 Searching company information...",
    "🌐 Crawling website...",
    "📄 Extracting content...",
    "🤖 Analyzing with AI...",
    "🏢 Finding competitors...",
    "📑 Generating PDF report...",
];

export default function Loader() {
    const [step, setStep] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setStep((prev) => {
                if (prev >= STEPS.length - 1) {
                    return prev;
                }

                return prev + 1;
            });
        }, 1800);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="rounded-xl bg-white p-8 shadow-lg">

            <div className="flex flex-col items-center gap-6">

                <Loader2
                    size={48}
                    className="animate-spin text-blue-600"
                />

                <div className="text-center">

                    <h2 className="text-xl font-semibold">
                        Researching Company
                    </h2>

                    <p className="mt-2 text-gray-600">
                        {STEPS[step]}
                    </p>

                </div>

                <div className="w-full">

                    <div className="h-2 overflow-hidden rounded-full bg-gray-200">

                        <div
                            className="h-full rounded-full bg-blue-600 transition-all duration-500"
                            style={{
                                width: `${
                                    ((step + 1) / STEPS.length) * 100
                                }%`,
                            }}
                        />

                    </div>

                    <div className="mt-2 text-center text-sm text-gray-500">

                        Step {step + 1} of {STEPS.length}

                    </div>

                </div>

            </div>

        </div>
    );
}