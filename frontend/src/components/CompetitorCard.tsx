import { ExternalLink, Globe } from "lucide-react";

interface Competitor {
    name: string;
    website: string;
    source: string;
}

interface Props {
    competitors: Competitor[];
}

export default function CompetitorCard({
    competitors,
}: Props) {
    if (!competitors || competitors.length === 0) {
        return (
            <div className="rounded-xl bg-white p-6 shadow-lg">
                <h2 className="mb-4 text-xl font-bold">
                    Competitors
                </h2>

                <p className="text-gray-500">
                    No competitors found.
                </p>
            </div>
        );
    }

    return (
        <div className="rounded-xl bg-white p-6 shadow-lg">

            <div className="mb-6 flex items-center justify-between">

                <h2 className="text-xl font-bold">
                    Competitors
                </h2>

                <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                    {competitors.length} Found
                </span>

            </div>

            <div className="grid gap-4 md:grid-cols-2">

                {competitors.map((competitor) => (

                    <div
                        key={competitor.name}
                        className="rounded-lg border p-5 transition hover:shadow-md"
                    >

                        <div className="mb-4 flex items-start justify-between">

                            <div>

                                <h3 className="text-lg font-semibold">
                                    {competitor.name}
                                </h3>

                                <span className="mt-1 inline-block rounded bg-gray-100 px-2 py-1 text-xs text-gray-600">
                                    {competitor.source}
                                </span>

                            </div>

                            <Globe
                                className="text-blue-600"
                                size={22}
                            />

                        </div>

                        {competitor.website ? (

                            <a
                                href={competitor.website}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 break-all text-blue-600 hover:underline"
                            >
                                {competitor.website}

                                <ExternalLink
                                    size={16}
                                />

                            </a>

                        ) : (

                            <p className="text-gray-500">
                                Website unavailable
                            </p>

                        )}

                    </div>

                ))}

            </div>

        </div>
    );
}